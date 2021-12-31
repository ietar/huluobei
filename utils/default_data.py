# -*- coding: utf-8 -*-
from copy import deepcopy


def n_data() -> dict:
    """
    正常数据 normal_data
    :return:
    """
    d = {}
    d.update(n_data_origin)
    return d


def e_data() -> dict:
    """
    异常型数据 error_data
    :return:
    """
    d = {}
    d.update(e_data_origin)
    return d


def j_data() -> dict:
    """
    跳转型数据 jump_data
    :return:
    """
    d = {}
    d.update(j_data_origin)
    return d


n_data_origin = {
    'result': True,
    'data': '',
    'msg': '',
}

e_data_origin = {
    'error_info': '',
    'return_page': '/',
    'return_text': '回首页',
}

j_data_origin = {
    'count_down': 5,
    'target_page': '/',
    'target': '首页',
    'msg': '',
}
