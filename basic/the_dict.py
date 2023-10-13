#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python内置了字典：dict的支持，dict全称dictionary，在其他语言中也称为map，使用键-值（key-value）存储，具有极快的查找速度。
"""

d = {"Michael": 95, "Bob": 75, "Tracy": 85}

print(d["Michael"])

"""
如果key不存在，dict就会报错：

>>> d['Thomas']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'Thomas'
"""

"""
要避免key不存在的错误，有两种办法，一是通过in判断key是否存在：
>>> 'Thomas' in d
False
"""

"""
二是通过dict提供的get()方法，如果key不存在，可以返回None，或者自己指定的value：
"""
print(d.get("Michael"))

"""
要删除一个key，用pop(key)方法，对应的value也会从dict中删除：
"""
print(d)
d.pop("Michael")
print(d)

d_empty = {}

print(d_empty.get("aa"))
