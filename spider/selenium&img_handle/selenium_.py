# -*- coding: utf-8 -*-
"""
动态页面获取：（phantomjs，selenium）
selenium : 是一个用于Web应用程序测试的工具。Selenium测试直接运行在浏览器中,就像真正的用户在操作一样。
phantomjs : PhantomJS 是一个基于 Webkit 的“无界面”(headless)浏览器非 Python 库，它会把网
站加载到内存并执行页面上的 JavaScript，不会展示图形界面。(官方已停止维护，可直接使用chomedriver作为驱动)
1. 由于如果需要使用selenium的话，需要为本机配置对应浏览器的驱动，下面以chomedriver为例，首先安装chromedriver，根据“对应版本”：http://npm.taobao.org/mirrors/chromedriver/
2. 下载后chromedriver，将exe文件放到谷歌浏览器的位置一样的目录下以及也要在python36/目录下也放置一份，并配置环境变量（不配置的话，需要在“webdriver.Chrome()”中指定位置）
3. cmd管理员下 pip install selenium
"""
"""
selenium优点：
	渲染数据，加载js，支持移动测试，广泛的支持语言，平台和浏览器，大型插件库
selenium缺点：
	没有内置的图像比较（Sikuli基于图像的识别工具），效率低，没有自带的报告功能，需要第三方插件完成
"""
"""   抓取英雄联盟壁纸   """
from selenium import webdriver
from urllib import request
import time
import os

hero = []
# 实例化一个浏览器驱动
brower = webdriver.Chrome()
# 用get打开对应网址
brower.get('http://lol.qq.com/web201310/info-heros.shtml')
# 根据情况给网页响应时间
time.sleep(3)
# 执行js：“window.scrollBy(0,1500)”，向下滚动1500px
brower.execute_script("window.scrollBy(0,1500)")
# 获取对应节点 (id返回单个节点，返回的多的话是列表)
infor = brower.find_element_by_css_selector('#jSearchHeroDiv')
links = infor.find_elements_by_css_selector('li>a')

for link in links:
	# get_attribute获取对应节点的属性值
	urls = link.get_attribute('href')
	hero.append(urls.split())
# print(hero)
for m in range(len(hero)):
	# print(hero[m][0])
	# 再打开单独英雄的壁纸链接
	brower.get(hero[m][0])
	# 数据缓冲
	time.sleep(2)
	# 执行js，左移100px，下移800px
	brower.execute_script("window.scrollBy(100,800)")
	# 找到对应的节点并点击
	brower.find_element_by_css_selector('#skinNAV').find_elements_by_css_selector('li a')[1].click()
	skins = brower.find_element_by_css_selector('#skinBG').find_elements_by_css_selector('li')
	for skin in skins:
		skin_name = skin.get_attribute('title')
		img_url = skin.find_element_by_css_selector('img').get_attribute('src')
		if '默认皮肤' in skin_name:
			skin_name = '默认皮肤_' + hero[m][0].split('?')[1].split('=')[1]
		else:
			skin_name = skin_name.replace(" ","_")
		if "/" in skin_name:
			skin_name = skin_name.replace("/", "-")
		print(skin_name)
		if not os.path.exists("lol_wallpaper"):
			os.mkdir("lol_wallpaper")
		request.urlretrieve(img_url, "lol_wallpaper/%s" % (skin_name + ".jpg"))