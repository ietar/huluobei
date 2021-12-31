# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from fdfs_client.client import Fdfs_client, get_tracker_conf


logger = logging.getLogger('django')


class FdfsStorage(FileSystemStorage):

    def url(self, name):
        """
        全路径
        :param name:
        :return:
        """
        return settings.__getattr__('CUSTOM_STORAGE_BASE_URL') + name

    def save(self, name, content, max_length=None):
        # 现在修好了 直接跳掉原来的保存过程 返回个新name就行 2021.12.10 17:57
        conf = get_tracker_conf(f'{settings.BASE_DIR}/utils/fastdfs/client.conf')
        client = Fdfs_client(conf)
        # res = client.upload_by_buffer(filebuffer=content.file.read())
        res = client.upload_by_buffer(filebuffer=content.file.read(), file_ext_name=name.split('.')[-1])

        new_name = res['Remote file_id'].decode()
        logger.info(f'上传文件至fdfs {res} name:{name} new_name: {new_name}')
        return str(new_name).replace('\\', '/')

    # def save(self, name, content, max_length=None):
    #     """
    #     Save new content to the file specified by name. The content should be
    #     a proper File object or any Python file-like object, ready to be read
    #     from the beginning.
    #     """
    #     # Get the proper name for the file, as it will actually be saved.
    #     if name is None:
    #         name = content.name
    #
    #     if not hasattr(content, 'chunks'):
    #         content = File(content, name)
    #
    #     name = self.get_available_name(name, max_length=max_length)
    #     return self._save(name, content)
