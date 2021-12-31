# -*- coding: utf-8 -*-
import copy
# import json
import logging
import random
import re
# import typing as _t

from captcha.image import ImageCaptcha, random_color as rc
from django.conf import settings
from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
# from django_redis import get_redis_connection
from rest_framework.views import APIView

# from utils.crypto import load_cookie_carts

logger = logging.getLogger('django')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_key_by_value(dic: dict, value):
    values = list(dic.values())
    try:
        index = values.index(value)
    except ValueError:
        return None

    return list(dic.keys()).__getitem__(index)


def ip2int(_ip: str) -> int:
    """
    ipv4
    :param _ip:
    :return:
    """

    parts = _ip.split('.')
    res = 0
    res += int(parts[0]) << 24
    res += int(parts[1]) << 16
    res += int(parts[2]) << 8
    res += int(parts[3])
    return res


def int2ip(_int: int) -> str:
    """
    ipv4
    :param _int:
    :return:
    """
    res = '.'.join([str(_int >> (i * 8) & 0xFF) for i in range(3, -1, -1)])
    return res


def digit_chars(length=6):
    digits = '1234567890'
    res = ''.join(random.choices(digits, k=length))
    return res


def list_sub(list1: list, list2: list) -> list:
    """
    列表减法 保持顺序
    :param list1: 被减数列表
    :param list2: 减数列表
    :return:
    """
    res = copy.deepcopy(list1)
    for item in list2:
        if item in list1:
            res.remove(item)
    return res


def mk_chars(length=4, exceptions=settings.__getattr__('CHAR_EXCEPTIONS') or 'ioszl10', lower_only=True,
             digit_more=False) -> str:
    """
    生成随机字母数字字符串 a-zA-Z0-9 排除exceptions字符的大小写 数字权重默认较低
    :param length: 生成字符串长度
    :param exceptions: 排除不易辨认的字符
    :param lower_only: 只包含小写字母
    :param digit_more: 数字与字母等量
    :return:
    """
    exceptions = exceptions.lower()
    all_chars = 'abcdefghijklmnopqrstuvwxyz'
    uppers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '1234567890'

    all_chars += digits
    if not lower_only:
        all_chars += uppers
    if digit_more:
        all_chars += digits

    for char in exceptions:
        all_chars = all_chars.replace(char, '')
        all_chars = all_chars.replace(char.upper(), '')
    res = ''.join(random.choices(all_chars, k=length))
    return res


def make_default_captcha(chars: str, color=(128, 255, None), bg=(0, 128, 50), noise=True, noise_color=None):
    """
    生成
    :param chars: 验证码字符串
    :param color: rgb的begin end opacity
    :param bg: rgb的begin end opacity
    :param noise: 是否带噪音
    :param noise_color: 噪音颜色 形式同color
    :return:
    """
    a = chars
    i = ImageCaptcha()
    b = rc(*bg)
    c = rc(*color)
    img = i.create_captcha_image(chars=a, color=c, background=b)
    if noise:
        img = i.create_noise_curve(image=img, color=noise_color or c)
    return img


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'header_key': 'Authorization',
        'token_format': 'jwt {token}',
        'token': token,
        'username': user.username,
        'id': user.id
    }


def get_user(account: str, user_model: AbstractUser):
    """
    :param user_model:
    :param account: username or mobile
    :return:
    """
    try:
        if not re.match(r'^1[3-9]\d{9}$', account):
            user = user_model.objects.get(username=account)
        else:
            user = user_model.objects.get(mobile=account)
    except ObjectDoesNotExist:
        return None
    return user


# class UsernameMobileBackend(ModelBackend):
#     """
#     自定义用户认证后端
#     """
#
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         """
#         :param request:
#         :param username: username or password
#         :param password:
#         :param kwargs:
#         :return:
#         """
#         user_model = get_user_model()
#         if username is None:  # jwt
#             username = kwargs.get(user_model.username)
#         if username is None or password is None:
#             return None
#
#         user = get_user(account=username, user_model=user_model)
#         if user and user.check_password(password) and user.is_active:
#             return user
#         else:
#             return None


class LoginRequiredJsonMixin(LoginRequiredMixin):
    # origin
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return self.handle_no_permission()
    #     return super().dispatch(request, *args, **kwargs)

    # fix
    def dispatch(self, request, *args, **kwargs):
        if isinstance(self, APIView):
            temp = APIView.dispatch(self, request, *args, **kwargs)
            _request = self.__getattribute__('request') or request
            if not _request.user.is_authenticated:
                return self.handle_no_permission()
            return temp
        else:
            if not request.user.is_authenticated:
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        data = {
            'result': False,
            'data': '',
            'msg': 'Unauthorized'
        }
        return JsonResponse(data, status=401)


if __name__ == '__main__':
    # _ip = ip2int('127.0.0.1')
    # print(_ip, type(_ip))
    # add = int2ip(_ip)
    # print(add, type(add))
    #
    # for test in range(1, 3000):
    #     try:
    #         test_ip = int2ip(test)
    #         test_int = ip2int(test_ip)
    #         if test_int != test:
    #             print(test)
    #     except IndexError as e:
    #         print(f'{e} {test}')
    #         input('continue?:')
    #         continue
    # print(ip2int('127.0.0.1'))
    # print(int2ip(4294967295))

    # a1 = get_key_by_value({'1': '123', '2': '223'}, '223')
    # a2 = get_key_by_value({'1': '123', '2': '223'}, '224')
    # a3 = get_key_by_value({'1': '123', '2': '223'}, '225')
    # print(a1, a2, a3)
    pass
