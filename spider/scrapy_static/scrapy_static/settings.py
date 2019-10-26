# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_static project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
BOT_NAME = 'scrapy_static'

SPIDER_MODULES = ['scrapy_static.spiders']
NEWSPIDER_MODULE = 'scrapy_static.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_static (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True      # 限定爬虫程序可以爬取的内容范围

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3    # 限制request请求时间间隙
DOWNLOAD_TIMEOUT = 60  # 60s内没有爬取下来网页，就放弃这个网页
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False    # 如果爬取的网站无需登录，就禁止cookie，防止了可能使用cookies识别爬虫轨迹的网站得逞

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scrapy_static.middlewares.ScrapyStaticSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# 设置代理中间件
DOWNLOADER_MIDDLEWARES = {
   'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
   'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware':None,
    # 'scrapy_static.middlewares.ScrapyStaticDownloaderMiddleware': 543,
    'scrapy_static.middlewares.RandomUserAgentMiddleware': 1,
    'scrapy_static.middlewares.RandomProxyIpSpiderMiddleware': 2,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 注册指定的Item管道,注意该方式注册的管道是一个全局管道,所有爬虫都可以共享该管道
# 后面的数字，是决定了管道的优先级，当spider返回item的时候，先执行哪个管道类，值越小越优先执行，
# 所以才可以在管道类中根据数据库判断图片是否已经下载过
ITEM_PIPELINES = {
    'scrapy_static.pipelines.ScrapyStaticPipeline': 300,
    'scrapy_static.pipelines.DownloadImage': 277,
}
# 配置图片存储的根路径,注意如果该路径不设置,此时即使添加了对应的图片处理管道,该管道也不会下载图片
IMAGES_STORE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'img')

#  配置图片缩略图，配置后会自动生成对应尺寸的图片，存到以key值命名的文件夹
# IMAGES_THUMBS = {
#     'small': (50, 50),
#     'big': (270, 270)
# }

# 配置过期时间
IMAGES_EXPIRES = 30  # 30天内抓取的都不会被重抓，默认90天

# 配置logging日志
"""
等级一次减小
CRITICAL - 严重错误(critical)
ERROR - 一般错误(regular errors)
WARNING - 警告信息(warning messages)
INFO - 一般信息(informational messages)
DEBUG - 调试信息(debugging messages)
"""
# 设置 WARNING 等级以下的log日志，不再显示
LOG_LEVEL = "WARNING"
# 配置log日志存储位置
LOG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'pipelines.log')

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
