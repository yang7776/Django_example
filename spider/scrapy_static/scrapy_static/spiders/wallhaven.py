# -*- coding: utf-8 -*-
import scrapy
import os
from spider.scrapy_static.scrapy_static.items import WallhavenItem
from scrapy_redis.spiders import RedisSpider        # 分布式导入
from scrapy_redis.spiders import RedisCrawlSpider   # 分布式导入，RedisCrawlSpider和正常类似，不用写make_requests_from_url


""" 爬取最大壁纸网站主页 wallhaven 首页分类图片 """

# 分布式写法（在settings中配置好后）
# class WallhavenSpider(RedisSpider):
#     name = 'wallhaven'
#     # 为爬虫定义一个从redis中提取任务的键，此后改爬虫会直接根据该键从链接的redis中提取任务
#     redis_key = 'distributed_db'
#     # 配置spider的log日志
#     custom_settings = {
#         # 设置管道下载
#         "ITEM_PIPELINES": {
#             'scrapy_static.pipelines.ScrapyStaticPipeline': 300,
#             'scrapy_static.pipelines.DownloadImage': 277,
#         },
#         # 设置log日志
#         "LOG_LEVEL": "WARNING",
#         "LOG_FILE": os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'spider.log')
#     }
#     """
#     make_request_from_data，make_requests_from_url作用都是可以帮助开发人员手动设置请求，但是不同之处是前者获取的请求链接是二进制数据类型，同时请求过程中不存在重复网址的过滤操作。但是后者直接获取的是请求的url，并且请求过程中存在重复链接的过滤操作。
#     """
#     # def make_request_from_data(self, data):
#     #      return scrapy.Request(url=data.decode('utf-8'), callback=self.parse)
#     def make_requests_from_url(self, url):
#         print("url is :%s"%url)
#         print("正在将任务加入队列，请稍等……")
#         return scrapy.Request(url=url, callback=self.parse)

# 正常写法
class WallhavenSpider(scrapy.Spider):
    """定义爬虫名称，爬取范围，爬取的第一个网址"""
    name = 'wallhaven'
    allowed_domains = ['wallhaven.cc']
    start_urls = ['https://wallhaven.cc/']
    
    # 配置spider的log日志
    custom_settings = {
        # 设置管道下载
        "ITEM_PIPELINES": {
            'scrapy_static.pipelines.ScrapyStaticPipeline': 300,
            'scrapy_static.pipelines.DownloadImage': 277,
        },
        # 设置log日志
        "LOG_LEVEL": "WARNING",
        "LOG_FILE": os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) ,'spider.log')
    }
    
    # 当网页下载成功之后,需要执行的回调函数,主要完成网页数据的解析
    def parse(self, response):
        # 获取图片类别的名称和链接
        type_names = response.xpath("//div[@class='pop-tags']/span/a/text()").extract()[:-1]
        type_links = response.xpath("//div[@class='pop-tags']/span/a/@href").extract()[:-1]
        for i in range(len(type_links)):
            for page in range(10): # 爬取十页图片
                yield scrapy.Request(
                    url = "{}&page={}".format(type_links[i],page+1),
                    meta = {"type_name":type_names[i]},
                    callback = self.parse_thumbnail
                )
                
    # 解析第二层缩略图链接
    def parse_thumbnail(self, response):
        # 获取缩略图链接
        img_link = response.xpath("//a[@class='preview']/@href").extract()
        for i in range(len(img_link)):
            yield scrapy.Request(
                url = img_link[i],
                meta={
                    "type_name": response.meta["type_name"]
                },
                callback=self.parse_img
            )
        
    # 解析图片信息
    def parse_img(self, response):
        # 获取图片标签
        tags = response.xpath("//ul[@id='tags']/li/a/text()").extract()
        # 获取图片尺寸信息
        size = response.xpath("//dl/dd[3]/text()").extract()[0]
        # 获取图片浏览量
        views = response.xpath("//dl/dd[4]/text()").extract()[0]
        # 获取图片链接
        img_link = response.xpath("//img[@id='wallpaper']/@src").extract()[0]
        print("正在解析：%s"%img_link)
        # 将数据构建成WallhavenItem实例
        img_item = WallhavenItem()
        img_item["id"] = img_link.split('-')[-1].split('.')[0]
        img_item["type"] = response.meta["type_name"]
        img_item["link"] = img_link
        img_item["tags"] = tags
        img_item["size"] = size
        img_item["views"] = views
        yield img_item