# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/14 16:58
# file_name     epoll_02.py
# coding:utf8
import gevent
from gevent import monkey
monkey.patch_all()  # 用于将标准库中大部分阻塞式调用修改为协作式运行，识别IO耗时操作

"""
gevent是一个基于协程的python网络库，在遇到IO阻塞时，程序会自动进行切换，可以让我们用同步的方式写异步IO代码。
即gevent的异步就是：按顺序发布的协程，但是不一定按顺序执行，会根据时间异步执行。
"""


def fetch(url):
    import requests
    print("get: {}".format(url))
    response = requests.get(url).content
    print("{}: {}".format(url, len(response)))


if __name__ == "__main__":
    gevent.joinall([
        gevent.spawn(fetch, "https://stackoverflow.com/"),
        gevent.spawn(fetch, "https://www.douban.com"),
        gevent.spawn(fetch, "https://www.github.com")
    ])

"""
不使用monkey.patch_all()后，运行结果：
	get: https://stackoverflow.com/
	https://stackoverflow.com/: 115049
	get: https://www.douban.com
	https://www.douban.com: 94578
	get: https://www.github.com
	https://www.github.com: 134566

使用monkey.patch_all()后，运行结果：
	get: https://stackoverflow.com/
	get: https://www.douban.com
	get: https://www.github.com
	https://www.douban.com: 94578
	https://www.github.com: 134571
	https://stackoverflow.com/: 115049

以上可以看到，当开启monkey.patch_all()，协程同时运行时，遇到IO耗时操作时，会根据耗时时间以此运行（上方的字节加载数是从小到大）
"""
