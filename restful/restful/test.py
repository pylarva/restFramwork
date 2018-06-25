# !/usr/bin/env python
# -*- coding:utf-8 -*-
# import types
#
# 1）是否可执行
# def func(args):
#     # if callable(args):
#     if isinstance(args, types.FunctionType):
#         print(args())
#     else:
#         print(args)
#
#
# func(123)
# func(lambda: 666)


# 2）__new__方法
class Foo(object):
    def __init__(self, a1):
        self.a = a1

    def __new__(cls, *args, **kwargs):
        """
        1) 首先执行类的__new__方法返回类的对象
        2）返回对象后 执行类的__init__方法
        :param args:
        :param kwargs:
        :return:
        """
        return object.__new__(cls)


obj = Foo(123)
print(obj)