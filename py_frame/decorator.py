# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/7/8 15:32
# file_name     decorator.py

import time
def phoenix(fn):
    """
    装饰器
    如果函数执行过程中出现异常，打印出错误信息并重新进入函数,
    重新进入前休眠1秒，防止程序一直出现异常导致占用过多CPU。
    """
    # @wraps(fn)
    def decorated(*args, **kwargs):
        while True:
            try:
                ret = fn(*args, **kwargs)
            except BaseException as e:
                print(e)
                time.sleep(1)
                continue
            return ret
    return decorated
# 不带参装饰器


def y_a(fun_a):
    def wrap():
        print(fun_a.__name__)
        return fun_a()
    return wrap


@y_a
def a():
    print("aaa")

# 带参数装饰器（其实就是无参装饰器外面在套一层）


def y_b(s):

    def wrap(fun):
        def f():
            print(s)
            return fun()
        return f

    return wrap


@y_b('this is a param')
def b():
    print("aaa")


a()
print('==========================================')
b()
