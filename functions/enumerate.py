"""
enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。

Python 2.3. 以上版本可用，2.6 添加 start 参数。

语法
以下是 enumerate() 方法的语法:
    enumerate(sequence, [start=0])

参数
    sequence -- 一个序列、迭代器或其他支持迭代对象。
    start -- 下标起始位置的值。

返回值
    返回 enumerate(枚举) 对象。
"""


def main():
    s = [1, 2, 3, 4, 5]
    e = enumerate(s)
    for i, v in e:
        print(f"index: {i}, value: {v}")


if __name__ == "__main__":
    main()
