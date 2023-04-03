#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from def_func import my_abs, power, power1, cal

print(max(1, 2, 5, 7))

print(my_abs(1))

print(power(1))

print('call power1 function, result: %d' % power1(2, 5))

# call calc function
print('call cal function, result: %d' % cal(1, 2))

nums = [1, 2, 3]
# *nums表示把nums这个list的所有元素作为可变参数传进去。
print('call cal function, result: %d' % cal(*nums))
