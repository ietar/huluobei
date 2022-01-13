# -*- coding: utf-8 -*-
import time
import traceback

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response

from crawlers.models import Book
from utils.any import logger
from utils.async_functions import async_get_content, sync_get_content
from utils.default_data import n_data


@sync_to_async
def get_content_view(request):
    # 爬内容了 自用
    res = n_data()

    try:
        # 校验

        u = request.user
        if not u.is_staff and not u.is_superuser:
            raise Exception('非管理员 无操作权限')

        get_dict = request.GET
        if not get_dict:
            raise Exception('id(book_id), prefix(biqooge的url prefix_book_id), target(爬几章)')
        book_id = get_dict.get('id') or 1
        prefix = get_dict.get('prefix') or 0
        try:
            target = int(get_dict.get('target', 1))
        except ValueError:
            raise Exception('target(爬取章节数)必须为整数')
        t1 = time.time()
        book1 = Book.objects.get(book_id=book_id)

    except ObjectDoesNotExist:
        res['result'] = False
        res['msg'] = '还没这本书的简介 先去get_chapter'
        return JsonResponse(res, status=400, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        res['result'] = False
        res['msg'] = str(e)
        return JsonResponse(res, status=400, json_dumps_params={'ensure_ascii': False})

    try:
        if book1.using:
            raise Exception('该书内容写入中 稍后再试')
        else:
            book1.using = True
            book1.save()
        async_get_content(book_id=book_id, current_chapter=book1.current, target=target, prefix=prefix)

        res['msg'] = f'已提交,当前待爬取章节数为 {book1.current + target}, 用时{round(time.time() - t1, 2)}秒'
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False})
        # return JsonResponse(res)

    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        book1.using = False
        book1.save()
        res['result'] = False
        res['msg'] = str(e)
        return JsonResponse(res, status=400, json_dumps_params={'ensure_ascii': False})
