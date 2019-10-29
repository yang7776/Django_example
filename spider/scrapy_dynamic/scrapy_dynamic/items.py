import scrapy

class Hero(scrapy.Item):
    model_name = scrapy.Field()
    kind = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    link = scrapy.Field()

class Shop(scrapy.Item):
    model_name = scrapy.Field()
    big_kind = scrapy.Field()
    small_kind = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()

class Skill(scrapy.Item):
    model_name = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    level = scrapy.Field()
    des = scrapy.Field()
    big_img = scrapy.Field()