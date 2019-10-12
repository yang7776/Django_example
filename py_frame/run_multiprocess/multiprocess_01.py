# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/12 15:33
# file_name     multiprocess.py
from multiprocessing import Process, Pool, Lock
# Process：进程类，用来创建进程对象
# Pool：进程池类，用来实现进程的批量创建
# Lock：进程锁，和线程的互斥锁使用相同，也是在对资源操作时，进行获取和释放。 进程锁使用实例：火车票抢票
import os
import time
# 定义函数，模仿进程需要执行的任务
"""
进程间同步：通过进程的join操作，实现下一个进程的执行需要等待上一个进程任务执行完毕。

进程间异步：多个进程之间分别执行自己的任务，互相之间无任何影响，进程完成的顺序无法预测。
"""


def task1(**kwargs):
    print(kwargs.get("name"))
    print(u'当前正在执行进程任务，正在执行的子进程编号为%s' % (os.getpid()))
    time.sleep(1)


if __name__ == '__main__':
    # 构建子进程
    # pro = Process(target=task1, kwargs={'name':'json'})
    # pro.start()     # 开启子进程
    # pro.join(timeout=7)     # 等待子进程结束后，再往下执行
    # print('任务执行完毕')

    # 创建进程池对象
    """
    进程池可以实现多个进程同步执行的操作， 并且方便管理多进程，
    其中apply_async用来向进程池中添加一个异步执行的进程。 apply则用来向进程池中添加一个同步执行的融进程。
    close：用来关闭进程池，一旦进程池调用close操作，此后，进程池不再接受任何进程任务。
    """
    pool = Pool(3)  # 允许进程池同时放入3个进程
    for i in range(5):
        # pool.apply(task1, kwds={'name': 'phone', 'age': '7'})    进程同步执行，不管进程池允许同时运行多少个，都是一个一个运行
        pool.apply_async(task1, kwds={'name': 'phone', 'age': '7'})   # 进程异步执行
    pool.close()
    pool.join()
