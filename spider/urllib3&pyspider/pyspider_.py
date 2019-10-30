# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/26 17:39
# file_name     pyspider_.py

from pyspider.libs.base_handler import *
import pymongo


class Handler(BaseHandler):
	# 对于整个爬虫项目的全局配置：所有的self.crawl()在请求的时候都会加载这个配置。
	crawl_config = {
	}
	# 创建mongo连接
	client = pymongo.MongoClient('127.0.0.1')
	db = client['pyspider_']
	
	# 项目启动首先进入的函数
	# @every: 用于设置定时爬取任务：可以是minutes, 也可以设置为seconds。
	# 24 * 60分 执行
	@every(minutes=24 * 60)
	def on_start(self):
		self.crawl('https://www.tripadvisor.cn/Attractions-g294212-Activities-oa30-Beijing.html#FILTERED_LIST',
				   callback=self.index_page)
	
	# 过期时间
	# age: 默认值是-1，永远不过期。主要是对任务url进行去重/过滤(根据taskid)，每一个url有唯一的一个标识taskid，age是一个以秒为单位的时间点，如果在这个时间范围内，遇到了相同的taskid，这个任务就会被丢弃。
	@config(age=10 * 24 * 60 * 60)
	def index_page(self, response):
		for each in response.doc('.more > a').items():
			self.crawl(each.attr.href, callback=self.detail_page)
		
		# 找到下一页
		next_href = response.doc('.next').attr.href
		self.crawl(next_href, callback=self.index_page)
	
	@config(priority=2)
	def detail_page(self, response):
		name = response.doc('h1').text()
		pls = response.doc('a > .reviewCount').text()
		address = response.doc(
			'#taplc_location_detail_contact_card_ar_responsive_0 > div.contactInfo > div.detail_section.address > span').text()
		phone = response.doc(
			'#taplc_location_detail_contact_card_ar_responsive_0 > div.contactInfo > div.contact > div.contactType.phone.is-hidden-mobile > div').text()
		kf_time = response.doc('.headerBL .header_detail').text()
		jj = response.doc('#component_3 > div > div:nth-child(2) > span:nth-child(1)').text()
		
		return {
			"url": response.url,
			"title": response.doc('title').text(),
			'名字': name,
			'评论数': pls,
			'地址': address,
			'手机': phone,
			'开放时间': kf_time,
			'简介': jj
		}
	
	# 自动调用
	# on_result是固定的函数，只要一个函数中有return，就会自动调用这个函数。
	def on_result(self, result):
		if result:
			self.save_mongo(result)
	
	def save_mongo(self, result):
		if self.db['beijing'].insert(result):
			print('保存到 mongo', result)