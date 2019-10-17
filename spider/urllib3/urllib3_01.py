# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/17 14:41
# file_name     zuiyou.py

import urllib3
import random

"""
urllib3是一个功能强大，条理清晰，用于HTTP请求的Python库，许多Python的原生系统都已经开始使用urllib3，urllib3提供了Python标准款库urllib中所没有的重要特性：
1、线程安全
2、链接池
3、客户端SSL/TLS验证
4、文件分部编码上传
5、协议处理重复请求和HTTP重定位
6、支持压缩编码
7、支持HTTP和SOCKS代理

参数：
	request(method, url, fields, headers):用来完成指定连接的数据请求，其中：
	method：设置请求方式，常用的请求方式为GET, POST
	url：设置请求的链接
	fields：设置对应请求需要发送的参数，该数据时字典类型，可以通过键值对设置
	headers：用来设置请求的头部信息，比如设置数据的编码格式，数据的参数类型，模拟浏览器发送请求等
"""

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 'Content-type': 'text/json'}
# 建立ip代理池
proxy_list = [
    'http://59.57.148.29:9999',
    "http://27.128.187.22:3128",
]
# 选择随机IP
ip = random.choice(proxy_list)

# 简单get请求
# http = urllib3.PoolManager(headers=header)

# 设置IP代理(使用IP代理爬取数据)
http = urllib3.ProxyManager(ip, proxy_headers=header)

"""
timeout=urllib3.Timeout(connect=3, read=3)：将连接的timeout和读的timeout分开设置。如果想让所有的request都遵循一个timeout，可以将timeout参数定义在PoolManager中

retries=urllib3.Retry(3, redirect=2)：进行3次请求重试，但是只进行2次重定向。如果想让所有请求都遵循一个retry策略，可以在PoolManager中定义retry参数
"""
response = http.request(
    'get',
    'http://www.baidu.com',
    timeout=urllib3.Timeout(connect=3, read=2),
    retries=urllib3.Retry(1, redirect=2))
print(response.status)
print(response.data.decode())

# 模拟浏览器发送请求
# 禁用urllib3警告（urllib3在进行https请求时，会抛出对应的警告，可以设置disable_warnings禁用对应的警告）
urllib3.disable_warnings()
