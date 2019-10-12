# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/12 16:52
# file_name     Rlock_and_Lock.py

# todo 互斥锁，死锁，递归锁，信号量，Condition（条件）

import threading
import time

"""
锁：意思主要是防止多个线程抢夺资源，最终产生脏数据，目的是为了保证数据的安全可靠性。
互斥锁：threading.Lock()，其实就是针对资源的操作进行获取锁和释放锁。
死锁：互斥锁对同一资源的操作，进行获取锁的次数大于释放锁的次数，即获取2次，释放1次，这样资源就会被一直锁。
递归锁：和互斥锁一模一样，只是对资源的操作锁几次都无所谓，只要最后释放锁就不会产生死锁。
信号量：其实和锁类似，只是上面的锁是一次只能一个线程进行，信号量是可以一次允许多个线程进行操作。
"""
# lock = threading.Lock()  # 互斥锁，实例化一个锁对象
# lock = threading.RLock()  # 递归锁，实例化一个锁对象
lock = threading.Semaphore(5)  # 信号量，实例化信号量对象

num = 0
t_obj = []


def run(n):
	print("task", n, threading.current_thread())
	lock.acquire()  # 获取锁
	global num
	num += 1
	print(num)
	lock.release()  # 释放锁

for i in range(3):
	t = threading.Thread(target=run, args=("t-%s" % i,))
	t.start()
	t_obj.append(t)

for t in t_obj:
	t.join()

print("num:", num)
