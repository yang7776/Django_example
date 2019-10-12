# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/12 16:25
# file_name     threading_03.py

# todo 计算子线程执行的时间以及统计当前活跃的线程数，sleep的时候是不会占用cpu的,在sleep的时候操作系统会把线程暂时挂起。

import threading
import time

"""
join()                          # 等此线程执行完后，再执行其他线程或主线程
threading.current_thread()      # 输出当前线程
threading.active_count()        # 输出当前活跃的线程数
"""


def run(n):
	print("task", n, threading.current_thread())  # 输出当前的线程
	time.sleep(1)
	print('3s')
	time.sleep(1)
	print('2s')
	time.sleep(1)
	print('1s')


strat_time = time.time()

t_obj = []  # 定义列表用于存放子线程实例

for i in range(3):
	t = threading.Thread(target=run, args=("t-%s" % i,))
	t.start()
	t_obj.append(t)

for tmp in t_obj:
	tmp.join()  # 为每个子线程添加join之后，主线程就会等这些子线程执行完之后再执行。

print("子线程花费时间:", time.time() - strat_time)  # 主线程
print(threading.active_count()) #输出当前活跃的线程数
print(threading.current_thread())  # 输出当前线程
