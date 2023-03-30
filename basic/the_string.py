#!/usr/bin/env python3
# -*- coding: utf-8 -*-

str = 'Hello, %s' % 'world'
print(str)

print('Hi, %s, you have $%d.' % ('Michael', 100000))


# format
print('Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125))

def format_percentage(a, b):
    p = 100 * a / b
    if p == 0.0:
        q = '0%'
    else:
        q = f'%.2f%%' % p
    return q

# f-string
s1 = 72
s2 = 85
r = format_percentage(85-72, 72)
print(r)

r = 100 * (85-72) / 72
print(f'{r:.2f}%')