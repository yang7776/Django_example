# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/12 16:12
# file_name     threading_02.py

#todo 继承threading.Thread来自定义线程类，其本质是重构Thread类中的run方法

import threading
import time

class MyThread(threading.Thread):
    def __init__(self, n):
        super(MyThread, self).__init__()  # 重构run函数必须要写
        self.n = n

    def run(self):   # 注意：因为是重构Thread类中的run方法，所以方法名必须是“run”
        print("task", self.n)
        time.sleep(1)
        print('2s')
        time.sleep(1)
        print('1s')
        time.sleep(1)
        print('0s')
        time.sleep(1)


if __name__ == "__main__":
    t1 = MyThread("t1")
    t2 = MyThread("t2")

    t1.start()
    t2.start()