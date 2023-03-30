#!/usr/bin/env python3
# -*- coding: utf-8 -*-

classmates = ['Michael', 'Bob', 'Tracy']
print(classmates[-1])

# Append
classmates.append('Adam')
print(classmates)

# insert
classmates.insert(1, "Jack")
print(classmates)

# pop
classmates.pop()
print(classmates)

# list中可以是不同类型的元素
s = ['Apple', 123, True]
print(s)

# list元素也可以是另一个list
l = ['python', 'java', ['asp', 'php'], 'scheme']
print(l)