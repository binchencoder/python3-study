#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class Separator(Enum):
    LINE = 1
    WHITE = 2


print(Separator.LINE)
print(Separator.LINE.name)
print(type(Separator.LINE))
