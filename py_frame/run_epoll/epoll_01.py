# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/12 18:02
# file_name     epoll_01.py

# todo 协程：

"""
线程和进程的操作是由程序触发系统接口，最后的执行者是系统，它本质上是操作系统提供的功能。而协程的操作则是程序员指定的，
在Python通过yield提供了对协程的基本支持，但是不完全。而第三方的gevent为Python提供了比较完善的协程支持，人为的实现并发处理。

协程的适用场景：当程序中存在大量不需要CPU的操作时（IO耗时任务）。
常用第三方模块gevent和greenlet。（本质上，gevent是对greenlet的高级封装，因此一般用它就行，这是一个相当高效的模块。）

当一个greenlet遇到IO操作时，比如访问网络，就自动切换到其他的greenlet，等到IO操作完成，再在适当的时候切换回来继续执行。
由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO。
"""
"""
猴子补丁：在运行时动态修改已有的代码，而不需要修改原始代码。但是此补丁带了便利的同时也有搞乱源代码优雅的风险。
协程在运行时遇到IO耗时操作自动切换，即就是猴子补丁的原理。

线程：python的线程属于内核级别的，即由操作系统控制调度（如单线程遇到io或执行时间过长就会被迫交出cpu执行权限（GIL锁），切换其他线程运行）
协程：单线程内开启协程，一旦遇到io，就会从应用程序级别（而非操作系统）控制切换，以此来提升效率（非io操作的切换与效率无关）

gevent.spawn()方法会创建一个新的greenlet协程对象，并运行它
gevent.joinall()方法的参数是一个协程对象列表，它会等待所有的协程都执行完毕后再退出
"""

import gevent
from gevent import monkey
monkey.patch_socket()  # monkey.patch_socket()#猴子补丁代替python原有的socket


def f(n):
    for i in range(n):
        print(gevent.getcurrent(), i)
        """
        以下模拟IO：输出0，准备输出1的时候，有等待时间，所以直接执行第二个greenlet，以此类推，所以结果是000 111 222 ...
        如果没有“gevent.sleep(1)”，则没有耗时操作，所以就会以此输出：01234 01234 ...

        注意：实际代码里，我们不会用gevent.sleep()去切换协程，而是在执行到IO操作时，gevent自动切换
        """
        gevent.sleep(1)   # 休息一秒，模拟遇到IO状况，此时协程自动切换成其他的gevent。


g1 = gevent.spawn(f, 5)  # 实例化一个协程
g2 = gevent.spawn(f, 5)
g3 = gevent.spawn(f, 5)

# join()：将对应协程加入任务队列； joinall()：将多个协程（列表）加入到任务队列
gevent.joinall([g1, g2, g3])
# g1.join() ; g2.join() ; g3.join()
