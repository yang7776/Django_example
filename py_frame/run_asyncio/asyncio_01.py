# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/15 15:39
# file_name     asyncio_01.py

import threading
import asyncio
"""
asyncio提供了完善的异步IO支持；
异步操作需要在coroutine中通过yield from完成；
多个coroutine可以封装成一组Task然后并发执行。

注意：以下写法主要针对 python3.5 版本以下
"""

# 知识网址：https://www.liaoxuefeng.com/wiki/1016959663602400/1017970488768640
# 简单实例 + 说明
# 把一个generator标记为coroutine类型
@asyncio.coroutine
def hello():
    print("Hello world!")
    # 异步调用asyncio.sleep(1):
    r = yield from asyncio.sleep(1)
    print("Hello again!")

# 获取EventLoop:
loop = asyncio.get_event_loop()
# 执行coroutine
loop.run_until_complete(hello())
loop.close()


# 实例
@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()