# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/25 12:30
# file_name     begin_static.py

from scrapy import cmdline

# cmdline.execute('scrapy crawl wallhaven --nolog'.split())
# cmdline.execute('scrapy crawl wallhaven'.split())
cmdline.execute('scrapy crawl wallhaven -s JOBDIR=crawls/wallhaven-1'.split())
