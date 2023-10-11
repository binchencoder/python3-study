#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合Json格式
    :param self:
    :return:
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding="utf-8")
        except ValueError:
            return False
        return True
    else:
        return False


# json 字符串
employee_string = (
    '{"first_name": "Michael", "last_name": "Rodgers", "department": "Marketing"}'
)

# type 检查对象类型
print(type(employee_string))

# 字符串转为对象
if check_json_format(employee_string):
    print("check_json_format is True")
    json_object = json.loads(employee_string)

# 检测类型
print(type(json_object))
