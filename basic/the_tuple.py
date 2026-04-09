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
a = ("physics", "chemistry", 1997, 2000)
b = (1, 2, 3, 4, 5, 6)
c = a + b
print(f"a+b={c} \n")
print(f"a[0]:={a[0]}")
print(f"b[1:5]={b[1:5]} \n")
"""
元组中的元素值是不允许删除的，但我们可以使用del语句来删除整个元组
"""
del c

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
