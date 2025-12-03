#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python内置了字典：dict的支持，dict全称dictionary，在其他语言中也称为map，使用键-值（key-value）存储，具有极快的查找速度。
"""


def init():
    global d
    d = {"Michael": 95, "Bob": 75, "Tracy": 85}
    print(d["Michael"])


def foreach():
    for k, v in d.items():
        print(k, v)


def check():
    """
    1. 如果key不存在，dict就会报错：  >>> d['Thomas']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'Thomas'
    """

    """
    2. 要避免key不存在的错误，有两种办法：
        一是通过in判断key是否存在：
    >>> 'Thomas' in d
    False
    """
    if 'Thomas' in d:
        print("'Thomas' in d")

    """
    二是通过dict提供的get()方法，如果key不存在，可以返回None，或者自己指定的value：
    """
    print(f'如果key不存在，返回None: {d.get("Michael")}')
    print(f'如果key不存在，返回指定值: {d.get("Michael1", "Default Value")}')


def pop():
    """
    3. 要删除一个key，用pop(key)方法，对应的value也会从dict中删除：
    """
    print(f"删除前的值：", d)
    d.pop("Michael")
    print(f"删除后的值：", d)

    d_empty = {}

    print(d_empty.get("aa"))


def append():
    c = {'chenbin': 32}
    d.update(c)
    print(f"相加之后的值：", d)


if __name__ == '__main__':
    init()

    # 遍历
    foreach()

    # 检查key是否存在
    check()

    # 删除元素
    pop()

    # 相加
    append()
