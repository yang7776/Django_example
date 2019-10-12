# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/12 16:32
# file_name     threading_04.py

# todo 守护线程

import threading
import time

"""
这里使用setDaemon(True)把所有的子线程都变成了主线程的守护线程，因此当主进程结束后，子线程也会随之结束。所以当主线程结束后，整个程序就退出了。

被设置为守护线程，表示该线程是不重要的,进程退出时不需要等待这个线程执行完成。
这样做的意义在于：避免子线程无限死循环，导致退不出程序，也就是避免楼上说的孤儿进程。
"""

def run(n):
    print("task", n)
    time.sleep(1)       #此时子线程停1s
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')

for i in range(3):
    t = threading.Thread(target=run, args=("t-%s" % i,))
    t.setDaemon(True)   #把子进程设置为守护线程，必须在start()之前设置
    t.start()

time.sleep(0.5)     #主线程停0.5秒
print(threading.active_count()) #输出活跃的线程数