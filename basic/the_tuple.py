#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tuple
另一种有序列表叫元组：tuple。tuple和list非常类似，但是tuple一旦初始化就不能修改，比如同样是列出同学的名字：
"""

classmates = ("Michael", "Bob", "Tracy")
print(classmates)

"""
连接, a就变成了一个新的元组，它包含了a和b中的所有元素
"""
a = (1, 2, 3)
b = (4, 5, 6)
c = a + b
print(f"a+b={c}")

"""
复制
"""
print(("Hi!",) * 4)

"""
判断元素是否存在
"""
print(3 in (1, 2, 3))

"""
迭代
"""
for x in (1, 2, 3):
    print(x)
