# -*- encoding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/8/18 下午5:50
# @Author  : Yang

# 节流类方法

VISIT_RECORD = {}
from rest_framework.throttling import BaseThrottle
import time
class VisitThrottle(BaseThrottle):

    def __init__(self):
        self.history = None  # 记录IP访问的最后时间

    # 返回True：可以继续访问     返回False：表示访问频率太高，限制访问
    # 限制同一IP， 10s内只能访问3次
    def allow_request(self,request,view):  # 源码节流方法
        # 1、获取用户IP
        remote_addr = request.META.get('REMOTE_ADDR')
        # 2、判断用户IP是否已经记录，没有记录则直接返回True
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime,]
            return True
        # 3、读记录的IP记录，判断是否5秒内访问了3次
        history = VISIT_RECORD.get(remote_addr)
        self.history = history
        while history and history[-1] < ctime - 10:
            history.pop()
        # 4、如果访问记录小于3次，则把最新访问时间记录后，返回True
        if len(history) < 3:
            history.insert(0,ctime)
            return True
        return False

    # 当访问被限制时，返回需要等多少秒才可以访问
    def wait(self):

        # 计算用户需要等待的时间，以动态等待时间返回
        ctime = time.time()
        wait_time = 10 - (ctime - self.history[-1])  # 注意时间戳之间的运算一定加括号，这样算出来结果为“秒”
        return wait_time