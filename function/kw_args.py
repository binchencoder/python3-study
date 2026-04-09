#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。
def person(name, age, **kw):
    print("name:", name, "age:", age, "other:", kw)
    print(kw.get("city"))


print(person("chenbin", 31))

# name: Bob age: 35 other: {'city': 'Beijing'}
print(person("Bob", 35, city="Beijing"))

# name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
print(person("Adam", 45, gender="M", job="Engineer"))

extra = {"city": "Beijing", "job": "Engineer"}
print(person("Jack", 24, city=extra["city"], job=extra["job"]))
print(person("Jack", 24, **extra))


# 对于关键字参数，函数的调用者可以传入任意不受限制的关键字参数。至于到底传入了哪些，就需要在函数内部通过kw检查。
# 以person()函数为例，我们希望检查是否有city和job参数。
def person1(name, age, **kw):
    if "city" in kw:
        pass
    if "job" in kw:
        pass
    print("name:", name, "age:", age, "other:", kw)


print(person1("Jack", 24, city="Beijing", addr="Chaoyang", zipCode=123456))


def person2(name, age, *, city, job):
    print(name, age, city, job)


print(person2("Jack", 24, city="Beijing", job="Engineer"))


def person3(name, age, *args, city, job):
    print(name, age, args, city, job)


print(person3("Jack", 34, city="Beijing", job="Dev"))
