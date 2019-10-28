# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/17 15:17
# file_name     ip_spider.py


import random
import json
import urllib3
from spider.user_agent_util import PC_USER_AGENT
from lxml import html
import gevent
from gevent import monkey
monkey.patch_all()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 消除https警告
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
proxy_lucency_ips = []
proxy_anonymity_ips = []

# ip清洗（过滤出可以使用的ip）
def checkip(targeturl, ip):
    http = urllib3.ProxyManager(ip, proxy_headers=headers)
    try:
        response = http.request(
            'get',
            targeturl,
            timeout=urllib3.Timeout(connect=3, read=3),
            retries=urllib3.Retry(1, redirect=2)
        ).status
        if response == 200:
            return True
        else:
            return False
    except BaseException:
        return False


# 爬取免费代理ip
def get_ip(type, page, targeturl):  # ip类型,页码,目标url,存放ip的路径
    dict = {
        '1': 'http://www.xicidaili.com/nt/',  # xicidaili国内普通代理(透明)
        '2': 'http://www.xicidaili.com/nn/',  # xicidaili国内高匿代理
        '3': 'http://www.xicidaili.com/wn/',  # xicidaili国内https代理
        '4': 'http://www.xicidaili.com/wt/'   # xicidaili国外http代理
    }
    url = dict[str(type)] + str(page)
    headers["User-Agent"] = random.choice(PC_USER_AGENT)

    # 请求数据，并转化为HTML
    http = urllib3.PoolManager()
    # 一下设为IO耗时任务
    ip_html = http.request("get", url, headers, timeout=5)
    element = html.etree.HTML(ip_html.data)

    # 获取返回html数据的指定节点并拼接
    ip_host = element.xpath("//table[@id='ip_list']//tr//td[2]/text()")
    ip_port = element.xpath("//table[@id='ip_list']//tr//td[3]/text()")
    ip_anonymity = element.xpath("//table[@id='ip_list']//tr//td[5]/text()")
    ip_type = element.xpath("//table[@id='ip_list']//tr//td[6]/text()")
    ip_live_time = element.xpath("//table[@id='ip_list']//tr//td[9]/text()")
    min_num = min(len(ip_host), len(ip_port), len(ip_type))

    # 检测ip可用性，并写入文档
    for i in range(min_num):
        ip = "{}://{}:{}".format(ip_type[i].lower(), ip_host[i], ip_port[i])
        is_avail = checkip(targeturl, ip)
        if not is_avail:
            print("此IP不可用:%s" % ip)
            continue
        else:
            ip_dic = {"ip": ip, "live_time": ip_live_time[i]}
            if "天" not in ip_live_time[i]:
                ip_dic["short_life"] = True
            else:
                ip_dic["short_life"] = False
            print("此IP可用:%s" % ip)
            if ip_anonymity == "透明":
                proxy_lucency_ips.append(ip_dic)
            else:
                proxy_anonymity_ips.append(ip_dic)


if __name__ == '__main__':
    tasks = []
    targeturl = 'http://www.baidu.com'    # 验证ip有效性的指定url
    for type in range(4):
        for page in range(10):
            # get_ip(type+1, page+1, targeturl)    # 同步
            tasks.append(gevent.spawn(get_ip, type + 1, page + 1, targeturl))  # 添加异步任务
    gevent.joinall(tasks)  # 执行协程异步任务
    with open("proxy_ip.json", "w+") as f:
        ip_json = {
            "lucency_ips": proxy_lucency_ips,
            "anonymity_ips": proxy_anonymity_ips
        }
        f.write(json.dumps(ip_json))
