#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Python内建的filter()函数用于过滤序列。
def is_odd(n):
    return n % 2 == 1


print(list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])))
