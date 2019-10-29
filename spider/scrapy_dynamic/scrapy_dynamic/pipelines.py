# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.conf import settings
from scrapy import Request
import pymongo

class DB:
    def start_connect(self):
        client = pymongo.MongoClient(settings['MONGO_HOST'],settings['MONGO_PORT'])
        db = client[settings['MONGO_DB']]
        self.col = db[settings['MONGO_COLNAME']]

    # 判断数据是否存在
    def or_exist(self,title):
        result = self.col.find({'title':title}).count()
        if result == 0:
            return False
        else:
            return True

    # 判断插入数据库时，数据是否重复
    def or_repeat(self, title, kind):
        result = self.col.find({'title': title, 'kind': kind}).count()
        if result == 0:
            return False
        else:
            return True

class Spider6Pipeline(object):
    def process_item(self, item, spider):
        return item

class DownloadImage(ImagesPipeline,DB):
    def get_media_requests(self, item, info):
        if not hasattr(self,'col'):
            self.start_connect()
        dic = dict(item)
        if self.or_exist(dic['title']) is False:
            if dic['img_url'].startswith('http') is False:
                img_url = 'http:'+dic['img_url']
            if item['model_name'] == '英雄':
                dirname = 'hero'
            elif item['model_name'] == '物品':
                dirname = 'shop'
            else:
                dirname = 'skill'
            yield Request(url=img_url, meta={'dir_name':dirname,'img_name':img_url.split('/')[-1]})

    # 设置图片下载成功之后。图片存储的路径
    def file_path(self, request, response=None, info=None):
        # 获取文件和文件夹名字
        dir_name = request.meta['dir_name']
        img_name = request.meta['img_name']
        return "{0}/{1}".format(dir_name,img_name)

    # 当图片下载结束之后修改item数据元的数据
    def item_completed(self, results, item, info):
        if item['model_name'] == '英雄':
            dirname = 'hero'
        elif item['model_name'] == '物品':
            dirname = 'shop'
        else:
            dirname = 'skill'
        # 获取item图片的名字
        img_name = item['img_url'].split('/')[-1]
        item['img_url'] = 'http://127.0.0.1:8080/img/{0}/{1}'.format(dirname,img_name)
        # 将数据插入到数据库
        if self.or_repeat(item['title'],item['kind']) is False:
            self.col.insert(dict(item))
        return item