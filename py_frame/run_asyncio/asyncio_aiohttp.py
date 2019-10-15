# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/15 16:52
# file_name     asyncio_03.py

# todo aiohttp必须放在异步函数中使用

import asyncio

"""
asyncio可以实现单线程并发IO操作。如果仅用在客户端，发挥的威力不大。如果把asyncio用在服务器端(djangode view层)，
例如Web服务器，由于HTTP连接就是IO操作，因此可以用单线程+coroutine实现多用户的高并发支持。

asyncio实现了TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架。

注意aiohttp的初始化函数init()也是一个coroutine，loop.create_server()则利用asyncio创建TCP服务。
"""
import aiohttp, asyncio

"""
链接地址：https://blog.csdn.net/qq_31235811/article/details/93380242
"""

# 进行多次请求，并限制同时请求的数量
async def main(pool):  # 启动
    sem = asyncio.Semaphore(pool)
    async with aiohttp.ClientSession() as session:  # 给所有的请求，创建同一个session
        tasks = []
        [tasks.append(control_sem(sem, 'https://api.github.com/events?a={}'.format(i), session)) for i in range(10)]  # 十次请求
        await asyncio.wait(tasks)


async def control_sem(sem, url, session):  # 限制信号量
    async with sem:
        await fetch(url, session)


async def fetch(url, session):  # 开启异步请求
    async with session.get(url) as resp:
        json = await resp.json()
        print(json)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(pool=2))  # 限制同时请求的数量