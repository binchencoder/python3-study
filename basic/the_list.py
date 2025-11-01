#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://blog.csdn.net/bang152101/article/details/105702464

from itertools import zip_longest


def opt_list():
    classmates = ["Michael", "Bob", "Tracy"]
    print(classmates[-1])

    # Append
    classmates.append("Adam")
    print(classmates)

    # insert
    classmates.insert(1, "Jack")
    print(classmates)

    # pop()方法用于弹出列表的最后一个元素
    classmates.pop()
    print(classmates)

    # list中可以是不同类型的元素
    s = ["Apple", 123, True]
    print(s)

    # list元素也可以是另一个list
    l = ["python", "java", ["asp", "php"], "scheme"]
    print(l)

    # 方法1：使用for循环简单结构遍历
    print("遍历方法1: for l1 in l")
    for l1 in l:
        print(f"遍历list: {l1}")

    # 方法2：借用 range() 和 len() 函数遍历
    print("遍历方法1: for i in range(len(l))")
    for i in range(len(l)):
        print(i + 1, l[i])

    # 方法3：借用 enumerate() 函数遍历
    for i, l1 in enumerate(l):
        print(i + 1, l1)

    # 方法4：借用 iter() 函数遍历
    for l1 in iter(l):
        print(l1)


def group_list():
    """
    使用 zip_longest 分组，用 fillvalue 填充不足的元素
    注意：这会返回元组列表
    """

    data = [10, 20, 30, 40, 50, 60, 70]
    chunk_size = 3

    # 创建 chunk_size 个迭代器，每个迭代器都偏移一个位置
    args = [iter(data)] * chunk_size

    # zip_longest 会将这些迭代器合并，自动填充最短的
    grp_it = list(zip_longest(*args, fillvalue=""))
    for it in grp_it:
        for i in it:
            print(i)


if __name__ == '__main__':
    # opt_list()
    print(group_list())
