#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Student(object):
    pass


print(Student())
print(Student)


class Student1(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score


print(Student1("chenbin", "99").name)
