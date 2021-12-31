from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.views import APIView

from utils.any import mk_chars, make_default_captcha


class ImageCodeView(APIView):
    def get(self, request, uuid: str):
        chars = mk_chars()
        img = make_default_captcha(chars).resize(size=(80, 30))
        out = BytesIO()
        img.save(out, format='JPEG')

        redis_conn = get_redis_connection('verify_code')
        _time = settings.__getattr__('CAPTCHA_EXPIRE') or 300  # 不转int试试
        redis_conn.setex(name=f'img_code_{uuid}', time=_time, value=chars)
        return HttpResponse(out.getvalue(), content_type='image/jpg')
