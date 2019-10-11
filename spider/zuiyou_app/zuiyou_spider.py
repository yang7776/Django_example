# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/11 16:26
# file_name     zuiyou_spider.py

# 爬取最右app相关信息
from urllib import request
import json
import sys

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
        "User_Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
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
        forms["offset"] = i*20
        data = json.dumps(forms)
        parse(url,headers,data)

def _progress(block_num, block_size, total_size):
    '''回调函数
       @block_num: 已经下载的数据块
       @block_size: 数据块的大小
       @total_size: 远程文件的大小
    '''
    downplan = float(block_num * block_size) / float(total_size) * 100.0
    sys.stdout.write('\r>> 当前图片下载进度：%.f%%' % (downplan))
    sys.stdout.flush()

def parse(url,headers,data):
    """
    处理数据
    :param url: 请求地址
    :param headers:请求头
    :param data:参数
    :return:
    """
    req = request.Request(url=url, headers=headers, data=bytes(data, encoding="utf-8"))
    response = request.urlopen(req)
    res = response.read().decode("utf-8")
    res = json.loads(res)
    data_list = res['data']['list']
    for i in data_list:
        img_list = i['imgs']
        for j in img_list:
            imgs = j['urls']['origin']['urls'][0]
            print("  资源地址：%s"%(imgs))
            request.urlretrieve(imgs, "zuiyou_source/%s" % imgs.split("/")[-3] + ".jpg" , _progress)

if __name__ == '__main__':
    get_page()