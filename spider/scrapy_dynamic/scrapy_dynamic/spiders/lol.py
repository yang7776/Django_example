# -*- coding: utf-8 -*-
import scrapy, os, json
# SplashRequest专门用来生成基于Splash加载的网络请求
from scrapy_splash import SplashRequest
from lxml import etree
from spider.scrapy_dynamic.scrapy_dynamic.spiders.lua_js import *
from spider.scrapy_dynamic.scrapy_dynamic.items import *
# import base64   # 实现字符串和图片之间的转化

class LolSpider(scrapy.Spider):
    name = 'lol'
    allowed_domains = ['http://lol.qq.com']
    start_urls = ['http://lol.qq.com/data/info-heros.shtml','https://lol.qq.com/data/info-item.shtml#Navi','https://lol.qq.com/data/info-spell.shtml#Navi']

    def start_requests(self):
        titles = ['英雄','物品','召唤师技能']
        for i in range(len(titles)):
            url = self.start_urls[i]
            return self.hero_operate(url)

    def parse(self, response):
        dic = json.loads(response.body)
        if dic['model_name']=='英雄':
            for key,value in dic.items():
                if key != 'model_name':
                    et = etree.HTML(value)
                    img_urls = et.xpath('//ul[@id="jSearchHeroDiv"]/li/a/img/@src')
                    links = et.xpath('//ul[@id="jSearchHeroDiv"]/li/a/@href')
                    titles = et.xpath('//ul[@id="jSearchHeroDiv"]/li/a/p/text()')
                    for i in range(len(titles)):
                        hero = Hero()
                        hero['model_name'] = '英雄'
                        hero['kind'] = key
                        hero['img_url'] = img_urls[i]
                        hero['link'] = links[i]
                        hero['title'] = titles[i]
                        yield hero

    # 定义函数完成爬取英雄页面的数据
    def hero_operate(self,url):
        dic = {'Fighter':'战士','Mage':'法师','Assassin':'刺客','Tank':'坦克','Marksman':'射手','Support':'辅助'}
        # endpoint:设置splash渲染的方式，默认是render.html:即直接返回js渲染之后的网页，如果页面需要进行额外的js操作时，此时需要使用execute，execute可以保证js和lua脚本实现无缝融合
        # args:用来设置未来向lua脚本中传递的参数，默认有一个url，该url在未设置时指向发送请求的url，wait：页面加载过程中等待的时间，单位为秒
        yield SplashRequest(url=url,callback=self.parse,endpoint='execute',args={'lua_source':lua_hero, 'wait':7, 'kind_dic':dic,'model_name':'英雄'})