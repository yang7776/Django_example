# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/12 9:38
# file_name     zy_spider2.py

from urllib import request
import requests
import random
import json
import sys

# 建立ip代理池
proxy_list = [
    {'http': '59.57.148.29:9999', 'https': '59.57.148.29:9999'},
    {"http": "27.128.187.22:3128", "https": "27.128.187.22:3128"}
]


def get_page():
    url = "http://izuiyou.com/api/index/webrecommend"
    headers = {
        "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }
    data = {
        "ctn": 20,
        "offset": 0,
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
        data["offset"] = i * 20
        parse(url, headers, data)


def _progress(block_num, block_size, total_size):
    downplan = float(block_num * block_size) / float(total_size) * 100.0
    sys.stdout.write('\r>> 当前图片下载进度：%.f%%' % (downplan))
    sys.stdout.flush()


def parse(url, headers, data):
    ip = random.choice(proxy_list)
    try:
        response = requests.post(url=url, json=data, headers=headers, proxies=ip, timeout=3)
        res = response.content.decode("utf-8")
        res = json.loads(res)
        data_list = res['data']['list']
        for i in data_list:
            img_list = i['imgs']
            for j in img_list:
                imgs = j['urls']['origin']['urls'][0]
                print("\r资源地址：%s" % (imgs))
                # 将数据从对应的网址上下载到本地，以下即时把网址对应的url下载到本地文件夹中，_progress是下载完成后的回调函数
                request.urlretrieve(imgs, "zuiyou_source/%s" % imgs.split("/")[-3] + ".jpg", _progress)
    except Exception as e:
        print("异常IP：%s" % (ip.get("http")))
        print("异常信息：%s" % (e))


if __name__ == '__main__':
    get_page()
