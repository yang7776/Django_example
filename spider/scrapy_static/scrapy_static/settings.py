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

# JOB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'img')

# 配置图片存储的根路径,注意如果该路径不设置,此时即使添加了对应的图片处理管道,该管道也不会下载图片
IMAGES_STORE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'img')

SPIDER_MODULES = ['scrapy_static.spiders']
NEWSPIDER_MODULE = 'scrapy_static.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_static (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True      # 限定爬虫程序可以爬取的内容范围

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3    # 限制request请求时间间隙
DOWNLOAD_TIMEOUT = 30  # 60s内没有爬取下来网页，就放弃这个网页
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16        # 现有的最大请求数，对于任何单域同时进行。
#CONCURRENT_REQUESTS_PER_IP = 16            # 现有的请求的最大数量的同时执行任何单一的IP。

# Disable cookies (enabled by default)
COOKIES_ENABLED = False    # 如果爬取的网站无需登录，就禁止cookie，防止了可能使用cookies识别爬虫轨迹的网站得逞

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# 它是用于Scrapy的HTTP请求的默认标题。
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
   "scrapy.downloadermiddlewares.retry.RetryMiddleware":550,
    # 'scrapy_static.middlewares.ScrapyStaticDownloaderMiddleware': 543,
    'scrapy_static.middlewares.RandomUserAgentMiddleware': 500,
    # 'scrapy_static.middlewares.RandomProxyIpSpiderMiddleware': 177,    # 自定义ip代理类
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
""" 将一个Scrapy项目改造成Scrapy-Redis增量式爬虫 """
# 纯源生的它内部默认是用的以时间戳作为key（当然也可以自定义去重类），使用Redis的set集合来存储请求的指纹数据, 从而实现请求去重的持久化
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 增加了调度的配置, 作用: 把请求对象存储到Redis数据, 从而实现请求的持久化.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 配置调度器是否要持久化, 也就是当爬虫结束了, 要不要清空Redis中请求队列和去重指纹的set。如果是True, 就表示要持久化存储, 就不清空数据, 否则清空数据
SCHEDULER_PERSIST = True
# 如果需要把数据存储到Redis数据库中, 可以配置RedisPipeline

# redis配置(爬取数据时，自动连接存储key值)
REDIS_HOST = "localhost"
REDIS_PORT = 6379
# REDIS_PARAMS = {'password': 'xxx'}


# 注册指定的Item管道,注意该方式注册的管道是一个全局管道,所有爬虫都可以共享该管道
# 后面的数字，是决定了管道的优先级，当spider返回item的时候，先执行哪个管道类，值越小越优先执行，
# 所以才可以在管道类中根据数据库判断图片是否已经下载过
ITEM_PIPELINES = {
    'scrapy_static.pipelines.ScrapyStaticPipeline': 300,
    'scrapy_static.pipelines.DownloadImage': 277,
    # 把爬虫爬取的数据存储到Redis数据库中
    "scrapy_redis.pipelines.RedisPipeline": 400,
}

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

# scrapy中默认的request并发数是32，设置前最好测试一下，一般占CPU的80-90%为好
CONCURRENT_REQUESTS = 32

# 是否开启重试：对失败的HTTP请求进行重试会减慢爬取的效率，尤其是当站点响应很慢(甚至失败)时， 访问这样的站点会造成超时并重试多次。这是不必要的，同时也占用了爬虫爬取其他站点的能力。
RETRY_ENABLED = True
# 重试次数
RETRY_TIMES = 3
# 遇到什么http code时需要重试，默认是500,502,503,504,408，其他的，网络连接超时等问题也会自动retry
# RETRY_HTTP_CODECS = 500

# 禁止重定向：当进行通用爬取时，一般的做法是保存重定向的地址，并在之后的爬取进行解析。 这保证了每批爬取的request数目在一定的数量， 否则重定向循环可能会导致爬虫在某个站点耗费过多资源。
REDIRECT_ENABLED = False

# 设置爬虫中断时，从中断的地方开始爬取，此目录不能被其他spider共享，如果不希望从中断的地方开始运行，只需要将这个文件夹删除即可
# 当然，也可以执行命令：scrapy crawl somespider -s JOBDIR=crawls/somespider-1
# JOB_DIR = JOB_PATH

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5         # 开始下载时限速并延迟时间
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60          # 高并发请求时最大延迟时间
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
