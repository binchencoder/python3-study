#!/usr/bin/env python3
# -*- coding: utf-8 -*-

age = 3
if age >= 18:
    print('audit')
elif age >= 6:
    print('teenager')
else:
    print('kid')

s = input('birth: ')
birth = int(s)
if birth < 2000:
    print('00前')
else:
    print('00后')
