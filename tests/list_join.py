#!/usr/bin/env python3
# -*- coding: utf-8 -*-

my_list = ["a,b", "c", "d"]

my_str = ",".join(map(str, my_list))

print(my_str)


print(",".join(map(str, [])))
