#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def my_abs(x):
    if x >= 0:
        return x
    else: 
        return -x

def my_abs1(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x

# def power function
def power(x):
    return x * x

def power1(x, n):
    s = 1
    while n > 1:
        n = n - 1
        s = s * x
    return s