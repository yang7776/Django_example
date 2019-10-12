# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/12 17:18
# file_name     Condition.py

# todo Conditon: thread内置的高级锁对象,内部默认封装的是一个Rlock对象

import threading
import time
import random

"""
Condition内部封装的也是acquire和release操作,只不过该操作内部也是通过Rlock来间接
操作上锁和解锁过程.同时Condition内部封装了一个线程等待池,只要线程通过调用wait()方
法,此时线程会被自动丢到线程等待池中,直到另一个线程通过notify()/notifyAll()来唤醒
在等待中的线程

Condition一般适用于"两个线程"互相协作完成的任务.

注意notify(n)默认每次只唤醒一个线程,但是当指定n的值时,此时可以唤醒n个线程(不分先
后顺序).
"""
con = threading.Condition()


def change():
	print("正在执行change方法，将要被添加到线程等待池中")
	con.acquire()
	con.wait()
	print('等待完毕，change运行！')
	con.release()


def out():
	print("正在执行out方法，将要被添加到线程等待池中")
	con.acquire()
	con.wait()
	print('等待完毕，out运行！')
	con.release()


thread1 = threading.Thread(target=change, name='thread1')
thread2 = threading.Thread(target=out, name='thread2')
thread1.start()
thread2.start()

time.sleep(3)
con.acquire()
con.notify(2)
con.release()
print('等待线程开始执行')
