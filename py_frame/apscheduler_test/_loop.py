#!/usr/bin/env python

import _thread
from time import sleep, ctime


def loop0():
    print('开始循环0次在：', ctime())
    sleep(4)
    print('结束循环0次在：', ctime())


def loop1():
    print('开始循环1次在：', ctime())
    sleep(2)
    print('结束循环1次在：', ctime())


'''    
def main():
    print('开始于：',ctime())
    loop0()
    loop1()
    print('所有的任务都完成于：',ctime())
'''


def main():
    print('starting at:', ctime())
    _thread.start_new_thread(loop0, ())
    _thread.start_new_thread(loop1, ())
    # sleep(6)
    # print('all done at:', ctime())


if __name__ == '__main__':
    main()