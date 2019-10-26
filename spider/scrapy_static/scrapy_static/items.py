# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
"""
items.py:用来设置未来存储数据的数据源,在该文件中所有的数据源必须继承自scrapy.Item,该数据源的作用跟django中的models比较相似,但是不同之处是,该数据源中提供的数据没有django中丰富的数据类型,所有数据都是Field类型,并且该数据源未来构造实例并不是对象实例,而是字典类型的实例
"""


class WallhavenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()     # 图片唯一标识
    type = scrapy.Field()   # 图片分类
    link = scrapy.Field()   # 图片链接
    tags = scrapy.Field()   # 图片标签
    size = scrapy.Field()   # 图片尺寸
    views = scrapy.Field()  # 图片浏览量
