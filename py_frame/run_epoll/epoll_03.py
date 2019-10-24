# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/15 15:27
# file_name     epoll_03.py

# todo gevent通过socket补丁实现redis.py非阻塞,详情可见文件 “py_frame/sql_class/redis.py”

from gevent import socket as gsocket
import redis

redis.connection.socket = gsocket
r = redis.StrictRedis()
p = r.connection_pool