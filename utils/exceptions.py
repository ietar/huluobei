# -*- coding: utf-8 -*-
import traceback

from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.db import DatabaseError

from utils.default_data import n_data


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        traceback.print_exc()
        data = n_data()
        data['result'] = False
        if isinstance(exc, DatabaseError):
            data['data'] = str(exc)
            data['msg'] = '数据库异常'
            response = Response(data=data, status=503)  # status不知道用哪个
        else:
            data['data'] = str(exc)
            data['msg'] = '服务器内部异常'
            response = Response(data=data, status=500)

    return response
