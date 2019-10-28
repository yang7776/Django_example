# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from py_frame.sql_class.mongodb_cls import MongoData
from scrapy.pipelines.images import ImagesPipeline
import logging
import os
logger = logging.getLogger(__name__)


class Mongo(MongoData):
    def __init__(self):
        super(Mongo, self).__init__("localhost", 27017, "wallhaven", "recommend_img")


class ScrapyStaticPipeline(Mongo, object):

    # 接收爬虫返回后的item
    def process_item(self, item, spider):
        dic = dict(item)
        if spider.name == "wallhaven":
            img_item = self.find({"id": dic["id"]})
            if not img_item:
                self.insert(dic)
        else:
            pass

    # 当爬虫关闭时执行
    def close_spider(self, spider):
        if spider.name == "wallhaven":
            spider_num = self.col.count()
            print("执行完毕！成功爬取了%s条数据"%spider_num)


# 定义一个管道类用来处理图片，注意：在settings中必须配置”下载路径“，和自定义的DownloadImage管道类
class DownloadImage(ImagesPipeline, Mongo):

    # 当爬虫提交item之后执行该操作.通常在此操作中发送图片请求
    def get_media_requests(self, item, info):

        # 判断是否可以获取到图片链接
        if item.get("link"):
            # 判断是否已连接数据库
            if not hasattr(self, "col"):
                super(Mongo, self).__init__("localhost", 27017, "wallhaven", "recommend_img")
            # 判断该图片是否已经下载过
            if not self.find({"id": item.get("id")}):
                url = item.get("link")
                yield Request(
                    url=url,
                    meta={
                        "image_type": item.get('type'),
                        'image_name': "{}.{}".format(item.get('id'), url.split('-')[-1].split('.')[-1])
                    }
                )

    # 设置下载图片的存储路径(代码动态创建的路径)
    def file_path(self, request, response=None, info=None):
        dir_name = request.meta.get('image_type')
        img_name = request.meta.get('image_name')
        return '{0}/{1}'.format(dir_name, img_name)

    # item_completed:当每一个item对应的图片下载任务全部结束时调用,通常在该方法中完成对指定item的过滤操作
    def item_completed(self, results, item, info):
        try:
            flag, img_info = results[0]
            if not flag:
                logger.warning("链接为 {} 的图片下载失败".format(item.get("link")))
        except BaseException:
            logger.warning("下载失败：%s" % item["link"])
        finally:
            # 注意：必须return返回数据，此时返回的数据会去执行接下来的pipeline类方法
            return item
