# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/15 16:41
# file_name     asyncio_02.py

import asyncio

"""
为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。

请注意，async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：
	把@asyncio.coroutine替换为async；
	把yield from替换为await。
"""

# 对比
# 3.5 版本之前
@asyncio.coroutine
def hello_3_4():
	print("Hello world!")
	r = yield from asyncio.sleep(1)
	print("Hello again!")
	

# 3.5 版本之后
async def hello_3_5():
	print("Hello world!")
	# 遇到耗时的操作，await就会使任务挂起，继续去完成下一个任务
	r = await asyncio.sleep(1)
	print("Hello again!")
	
	
loop = asyncio.get_event_loop()
tasks = [hello_3_4(), hello_3_5()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()