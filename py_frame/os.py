# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/7/30 17:42
# file_name     test.py

import os
# 获取当前文件的绝对路径
path1 = os.path.abspath(__file__)

"""
获取当前文件父文件的绝对路径,等同于“os.path.dirname(os.path.abspath(__file__))”
注意：第二个中的参数，一个点代表“父级”，两个点代表“爷级”，“../..”代表“爷的父级”，以此类推
"""
path2 = os.getcwd()
path3 = os.path.abspath('.')

# “join”用来拼接指定路径和字符串，从而形成新的路径
path4 = os.path.join(path3, 'os.txt')

"""
如果以 r+、w、w+、a、a+ 模式打开文件，则都可以写入。需要指出的是，当以 r+、w、w+ 模式打开文件时，文件指针位于文件开头处；当以 a、a+ 模式打开文件时，文件指针位于文件结尾处。
"""
# 打开文件操作，“with open”和“os.open”的区别就是，with是自动关闭文件的。
try:
    with open(path4, 'r', encoding='utf-8') as f:
        print(f.read())
except FileNotFoundError:
    print('无法打开指定的文件!')
except LookupError:
    print('指定了未知的编码!')
except UnicodeDecodeError:
    print('读取文件时解码错误!')
# 写入文件操作
# with open(path4,'a') as f:
# 	f.write('this is a test/')

# print(path1)
# print(path2)
# print(path3)
# print(path4)
