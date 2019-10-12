# -*- coding: utf-8 -*-
"""
多进程模块为我们提供了一个更加高级的进程通信类Manager，该类支持比较丰富的数据结构。比如：list，dict，namespace等，Manager类是对Queue和Pipe更加高级的封装。能够轻松实现多进程之间的数据共享。
"""
from multiprocessing import Manager, Process


def write(dict, **kwargs):
    for key, value in kwargs.items():
        dict[key] = value
    print(dict)


def read(d):
    print(d)


if __name__ == '__main__':
    # 创建Manager对象
    manage = Manager()
    # 构建manage对象支持的数据类型
    d = manage.dict()
    pro1 = Process(target=write, args=(d,), kwargs={'name': 'xiaocai', 'age': 77})
    pro2 = Process(target=read, args=(d,))
    pro1.start()
    pro1.join()
    pro2.start()
    pro2.join()
