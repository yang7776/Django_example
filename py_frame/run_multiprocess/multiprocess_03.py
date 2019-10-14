# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/12 17:40
# file_name     multiprocess_04.py

# todo 进程间通信：由于进程之间数据是不共享的，所以不会出现多线程GIL带来的问题。多进程之间的通信通过Queue()或Pipe()来实现

from multiprocessing import Process, Queue, Pipe
"""
注意：
	Queue()或Pipe()是实现进程间的数据传递；
	Manager()是实现进程间的数据共享
"""

def queue(q):
	q.put([77, None, 'hello'])


def pipe(conn):
	conn.send([42, None, 'hello'])
	conn.close()


if __name__ == '__main__':
	# Queue通信
	# q = Queue()
	# p = Process(target=queue, args=(q,))
	# p.start()
	# print(q.get())  # prints "[42, None, 'hello']"
	# p.join()
	
	# Pipe通信
	parent_conn, child_conn = Pipe()
	p = Process(target=pipe, args=(child_conn,))
	p.start()
	print(parent_conn.recv())  # prints "[42, None, 'hello']"
	p.join()