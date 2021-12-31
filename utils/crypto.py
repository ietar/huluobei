# -*- coding: utf-8 -*-
import json, base64
import pickle


def dump_cookie_carts(before: dict) -> str:
    res1 = pickle.dumps(before)
    res2 = base64.b64encode(res1)
    res3 = res2.decode()
    return res3


def load_cookie_carts(before: str) -> dict:
    res1 = before.encode()
    res2 = base64.b64decode(res1)
    res3 = pickle.loads(res2)
    return res3


if __name__ == '__main__':
    a = {'name': 'ietar', 'id': 1}
    b = dump_cookie_carts(a)
    print(b)
    c = load_cookie_carts(b)
    print(c)
