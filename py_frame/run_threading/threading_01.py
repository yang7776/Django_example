# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/12 16:10
# file_name     threading_01.py

#todo 普通创建方式

import threading
import time

def run(n):
    print("task", n)
    time.sleep(1)
    print('2s')
    time.sleep(1)
    print('1s')
    time.sleep(1)
    print('0s')
    time.sleep(1)

# 创建线程对象
t1 = threading.Thread(target=run, args=("t1",))
t2 = threading.Thread(target=run, args=("t2",))
# 线程准备就绪，等待CPU调度，即执行线程
t1.start()
t2.start()