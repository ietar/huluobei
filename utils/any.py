# -*- coding: utf-8 -*-
import copy
import json
import logging
import random
import re
import typing as _t
from collections import OrderedDict

from alipay import AliPay
from captcha.image import ImageCaptcha, random_color as rc
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.http import JsonResponse
from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer as TimedJWSS
from rest_framework.views import APIView

from goods.models import GoodsChannel
from utils.crypto import load_cookie_carts

logger = logging.getLogger('django')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_alipay_object(settings: dict):

    alipay_settings = settings
    appid = alipay_settings.get('app_id')
    app_private_key = alipay_settings.get('app_private_key')
    alipay_public_key = alipay_settings.get('alipay_public_key')
    debug = alipay_settings.get('debug')

    obj = AliPay(appid=appid,
                 app_notify_url=None,
                 app_private_key_string=app_private_key,
                 alipay_public_key_string=alipay_public_key,
                 sign_type='RSA2',
                 debug=debug
                 )
    return obj


def get_key_by_value(dic: dict, value):
    values = list(dic.values())
    try:
        index = values.index(value)
    except ValueError:
        return None

    return list(dic.keys()).__getitem__(index)


def merge_carts(request, user):
    cookie_carts = request.COOKIES.get('carts')
    if cookie_carts:
        cookie_carts = load_cookie_carts(cookie_carts)
    else:
        cookie_carts = {}

    redis_conn = get_redis_connection('carts')
    redis_record = redis_conn.get(f'carts_{user.id}') or b'{}'
    redis_carts = json.loads(redis_record)

    for k, v in cookie_carts.items():
        if k in redis_carts:
            redis_carts['count'] += v['count']
            redis_carts['selected'] = redis_carts['selected'] or v['selected']
        else:
            redis_carts[k] = v

    redis_conn.set(name=f'carts_{user.id}', value=json.dumps(redis_carts))


def get_categories():
    o_dict = OrderedDict()
    t2s = GoodsChannel.objects.all().order_by('group_id', 'sequence')
    for t2 in t2s:
        t1 = t2.group_id
        if t1 not in o_dict:
            o_dict[t1] = {'channels': [], 'subs': []}

        cat1 = t2.category
        temp = {'id': cat1.id,
                'name': cat1.name,
                'url': t2.url
                }
        o_dict[t1]['channels'].append(temp)

        cat2s = cat1.subs.all().order_by('id')
        for cat2 in cat2s:
            temp2 = {'id': cat2.id, 'name': cat2.name, 'subs': []}

            cat3s = cat2.subs.all().order_by('id')
            for cat3 in cat3s:
                temp2['subs'].append({'id': cat3.id, 'name': cat3.name})

            o_dict[t1]['subs'].append(temp2)

    return o_dict


def check_verify_email_token(token: str) -> _t.Union[None, AbstractUser]:
    """

    :param token:
    :return: user or None
    """
    s = TimedJWSS(secret_key=settings.SECRET_KEY)
    try:
        data = s.loads(token)
    except Exception as e:
        logger.error(e)
        return None
    else:
        user_id = data.get('user_id')
        email = data.get('email')
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=user_id, email=email)
        except user_model.DoesNotExist:
            return None
        else:
            return user


def get_verify_email_url(user: AbstractUser, prefix: str) -> str:
    """
    生成验证邮箱的url
    :param prefix: domain 域名 通过request.META.get('HTTP_ORIGIN')获取
    :param user:
    :return:
    """
    # s = sl(secret_key=settings.SECRET_KEY, expires_in=settings.__getattr__('EMAIL_VERIFY_EXPIRATION'))
    s = TimedJWSS(secret_key=settings.SECRET_KEY)
    data = {
        'user_id': user.id,
        'email': user.email,
    }
    token = s.dumps(data).decode()
    url = prefix + settings.__getattr__('EMAIL_VERIFY_SUFFIX') + '?token=' + token
    return url


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
    except user_model.DoesNotExist:
        return None
    return user


class UsernameMobileBackend(ModelBackend):
    """
    自定义用户认证后端
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        :param request:
        :param username: username or password
        :param password:
        :param kwargs:
        :return:
        """
        user_model = get_user_model()
        if username is None:  # jwt
            username = kwargs.get(user_model.username)
        if username is None or password is None:
            return None

        user = get_user(account=username, user_model=user_model)
        if user and user.check_password(password) and user.is_active:
            return user
        else:
            return None


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

    pass
