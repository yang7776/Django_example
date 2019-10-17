# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/16 9:56
# file_name     asyncio_base.py

# async def async_func():
# 	return 1
#
def run(coroutine):
	try:
		coroutine.send(None)
	except StopIteration as e:
		print("=====  %s" % (e.value))
#
# async def await_coroutine():
# 	res = await async_func()
# 	print(res)
#
# run(await_coroutine())

import asyncio
"""
多进程+协程  爬取20W条数据例子
"""
# -*- coding=utf-8 -*-
import requests
from multiprocessing import Process
import gevent
from gevent import monkey
monkey.patch_all()

def fetch(url):
	try:
		s = requests.Session()
		r = s.get(url, timeout=1)  # 在这里抓取页面
	except Exception as e:
		print(e)
	return ''


def process_start(url_list):
	tasks = []
	for url in url_list:
		tasks.append(gevent.spawn(fetch, url))
	gevent.joinall(tasks)  # 使用协程来执行


def task_start(filepath, flag=100000):  # 每10W条url启动一个进程
	with open(filepath, 'r') as reader:  # 从给定的文件中读取url
		url = reader.readline().strip()
		url_list = []  # 这个list用于存放协程任务
		i = 0  # 计数器，记录添加了多少个url到协程队列
		while url != '':
			i += 1
			url_list.append(url)  # 每次读取出url，将url添加到队列
			if i == flag:  # 一定数量的url就启动一个进程并执行
				p = Process(target=process_start, args=(url_list,))
				p.start()
				url_list = []  # 重置url队列
				i = 0  # 重置计数器
			url = reader.readline().strip()
		if url_list:  # 若退出循环后任务队列里还有url剩余
			p = Process(target=process_start, args=(url_list,))  # 把剩余的url全都放到最后这个进程来执行
			p.start()


if __name__ == '__main__':
	task_start('./testData.txt')  # 读取指定文件
