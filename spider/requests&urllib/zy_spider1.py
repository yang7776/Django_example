# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/11 16:26
# file_name     zuiyou_spider.py

# 爬取最右app相关信息

from urllib import request
import json
import sys
import random
import socket
"""
爬取方式：主要是根据http请求爬取数据
"""


def get_page():
    """
    处理参数请求头
    :param url: 请求地址
    :param headers: 请求头
    :param data: 参数
    :return: NOne
    """

    url = "http://izuiyou.com/api/index/webrecommend"

    headers = {
        "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }
    forms = {
        "ctn": 20,
        "direction": "up",
        "filter": "imgtxt",
        "h_av": 3.0,
        "h_ch": "web_app",
        "h_dt": 9,
        "h_nt": 9,
        "tab": "rec",
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131Safari/537.36",
    }

    page = int(input("请输入要爬取多少页最右数据（一页20条数据）:"))
    for i in range(page):
        forms["offset"] = i * 20
        data = json.dumps(forms)
        parse(url, headers, data)


def _progress(block_num, block_size, total_size):
    '''回调函数
       @block_num: 已经下载的数据块
       @block_size: 数据块的大小
       @total_size: 远程文件的大小
    '''
    downplan = float(block_num * block_size) / float(total_size) * 100.0
    sys.stdout.write('\r>> 当前图片下载进度：%.f%%' % (downplan))
    sys.stdout.flush()


def parse(url, headers, data):
    """
    处理数据
    :param url: 请求地址
    :param headers:请求头
    :param data:参数
    :return:
    """
    """
    在urllib库中，给我们提供了一些Handler，如：HTTPHandler，HTTPSHandler，ProxyHandler，BaseHandler，AbstractHTTPHandler，FileHandler，FTPHandler，分别用于处理HTTP，HTTPS，Proxy代理等。
    """
    # 建立ip代理池
    proxy_list = [
        {'http': '59.57.148.29:9999'},
        {"http": "27.128.187.22:3128"}
    ]
    # 随机选择ip
    # proxy = random.choice(proxy_list)
    # 构建一个ProxyHandler处理器对象，支持IP代理处理
    proxy = request.ProxyHandler({'http': '59.57.148.29:9999'})
    # 创建支持代理池的opener对象（当使用复杂爬取方式时，如HTTPs，FTP, Proxy代理等，需要使用自定义opener）
    opener = request.build_opener(proxy)
    # 将代理IP设置成全局,当使用urlopen()请求时自动使用代理IP
    request.install_opener(opener)
    # 设置超时
    socket.setdefaulttimeout(1)
    
    try:
        # 建立一个请求，注意：参数必须是字节流类型
        req = request.Request(url=url, headers=headers, data=bytes(data, encoding="utf-8"))
        # 接收返回的response对象
        response = opener.open(req)  # 当使用opener时，就需要使用此方式来接收返回的数据
        # response = request.urlopen(req)
        # 读取response对象中的数据
        res = response.read().decode("utf-8")
        # json解析
        res = json.loads(res)
        data_list = res['data']['list']
    except Exception as e:
        data_list = []
        print(e)
    for i in data_list:
        img_list = i['imgs']
        for j in img_list:
            imgs = j['urls']['origin']['urls'][0]
            print("\r资源地址：%s" % (imgs))
            # 将数据从对应的网址上下载到本地，以下即时把网址对应的url下载到本地文件夹中，_progress是下载完成后的回调函数
            request.urlretrieve(imgs, "zuiyou_source/%s" % imgs.split("/")[-3] + ".jpg", _progress)


if __name__ == '__main__':
    get_page()
