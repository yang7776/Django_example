# -*- coding: utf-8 -*-

import logging
import os
import sys

LOG_PATH = os.getcwd()
sys.path.append(LOG_PATH)  # 定义log文件的存放路径

logger_test = logging.getLogger('test_log')   # log初始化，括号中一般填写模块名称，“logger_test”为log对象名称
logger_test.setLevel(logging.DEBUG)  # log打印有级别，将“debug”级别调为最高，不然输出时会被其他覆盖
fh = logging.FileHandler(LOG_PATH + '/test_log.log', encoding='utf-8')  # 设置日志文件的存储路径，注意后面的日志名称
formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(message)s')  # 设置输出的格式
fh.setFormatter(formatter)  # 设置输出的格式
logger_test.addHandler(fh)  # 设置最新log日志是以添加的方式，而不是以覆盖的方式存入文件，根据需求设置，若需要短时间保存，则需要执行此命令
# ……配置多个log模块

logger_test.debug('这是一个log测试')
logger_test.info('这是一个log测试')
logger_test.warning('这是一个log测试')
logger_test.error('这是一个log测试')
