# -*- coding: utf-8 -*-
import typing as _t


def missing_params(res: dict, source: dict, params: _t.Iterable) -> bool:
    """
    校验source中是否有所有参数 直接修改字典res 参数完整返回True 否则False
    :param res:
    :param source: 数据来源 request.data/request.GET/request.POST
    :param params: (str, str, ...)
    :return:
    """
    missing = [param for param in params if (source.get(param) is None)]

    msg = f"missing param: {' '.join(missing)}"
    if missing:
        res['result'] = False
        res['msg'] = msg
    return bool(missing)


if __name__ == '__main__':
    r = {}
    s = {'1': 2}
    p = ('1', '2', '3')
    a = missing_params(r, source=s, params=p)
    print(a, r)
