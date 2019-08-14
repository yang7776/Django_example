import os

# ADMINS = (
#     ('Mr Yang', 'ysh_7776@163.com'),  # 设置管理员邮箱
# )
#
# # Email
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.qq.com'  # QQ邮箱SMTP服务器
# EMAIL_PORT = 25  # QQ邮箱SMTP服务端口
# EMAIL_HOST_USER = '3152439509@qq.com'  # 我的邮箱帐号
# EMAIL_HOST_PASSWORD = 'whiejlxphifmdcib'  # 密码
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER

# 创建logs文件夹
cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path): os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个

# 配置信息
LOGGING = {
    'version': 1,    # 指明dictConnfig的版本，目前就只有一个版本
    'disable_existing_loggers': True,    # false：禁用已经存在的logger实例
    # 配置日志输出格式，下面的三种输出格式standard和simple，collect，其中collect是自己定义的格式，起码要有标准和简单两个格式
    'formatters': {
        # 日志标准输出格式
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        # 日志简单输出格式
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        # 定义一个特殊的日志格式
        'collect': {
            'format': '这是一个自定义格式 %(levelname)s %(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',   # 当setting的DEBUG = True时生效
        },
    },
    # 配置处理器，定义具体处理日志的方式
    'handlers': {
        # 在终端(控制台)输出日志，所以若项目上线，可在下面loggers中不选择
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 在定义的all.log文件中打印所有
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，根据文件大小自动切，即文件空间不足时，重新备份
            'filename': os.path.join(log_path, "info.log"),  # 日志文件，名字可自取
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 3,  # 最多备份几个
            'formatter': 'standard',    # 输出格式选择，可选择上面定义的其中一个
            'encoding': 'utf-8',    #编码格式
        },
        'info_time':{
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件，根据时间自动切，到设定时间时自动备份
            'filename': os.path.join(log_path, "info_time.log"),  # 日志文件
            'backupCount': 3,  # 备份数为3  xx.log --> xx.log.2018-08-23_00-00-00 --> xx.log.2018-08-24_00-00-00 --> ...
            'when': 'D',  # 每天一切， 可选值有S/秒 M/分 H/小时 D/天 W0-W6/周(0=周一) midnight/如果没指定时间就默认在午夜
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门用来记错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(log_path, "error.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(log_path, "collect.log"),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': "utf-8"
        },
        'debug': {#输出到文件
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'debug.log'),#日志输出文件
            'maxBytes':1024*1024*5,#文件大小
            'backupCount': 5,#备份份数
            'formatter':'standard',#使用哪种formatters日志格式
        },
        'mail_admins':{
            "level":'ERROR',
            "class":'django.utils.log.AdminEmailHandler',
            "include_html":True
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型为 django 处理所有类型的日志， 默认调用
        'django': {   # 定义实例时需要定义的名称
            # 默认记录系统日志并输出到控制台
            'handlers': ['info', 'console','error'],     # 上线之后可以把'console'移除
            'level': 'INFO',
            'propagate': True   # 向不向更高级别的logger传递
        },
        # log 调用时需要当作参数传入
        'collect': {
            # 配置手动添加的日志
            'handlers': ['console', 'collect'],
            'level': 'INFO',
            # 'propagate': True
        },

        'django.request': {
            'handlers': ['debug','mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    }
}
# formatters: 指定输出的格式，被handler使用。
# handlers： 指定输出到控制台还是文件中，以及输出的方式。被logger引用，其中handlers中还可以配置将错误日志以邮件形式发送给管理员
# loggers： 指定django中的每个模块使用哪个handlers。以及日志输出的级别。