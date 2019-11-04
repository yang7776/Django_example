# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/11/4 11:57
# file_name     routing.py

# todo routing.py类似于Django中的url.py,指明websocket协议的路由。
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from dj_study.channels_.consumers import ChatConsumer

"""
ProtocolTypeRouter： ASIG支持多种不同的协议，在这里可以指定特定协议的路由信息，我们只使用了websocket协议，这里只配置websocket即可

AuthMiddlewareStack： django的channels封装了django的auth模块，使用这个配置我们就可以在consumer中通过下边的代码获取到用户的信息

URLRouter： 指定路由文件的路径，也可以直接将路由信息写在这里，代码中配置了路由文件的路径，会去chat下的routeing.py文件中查找websocket_urlpatterns，chat/routing.py内容如下

注意：这不仅只适用于实时聊天，也适用于当使用“celery”来异步处理IO耗时任务时，前端的持续性连接，方便随时显示耗时任务的处理进度，不然就只能一直定时发ajax来确定处理进度，非常耗时和消耗资源。
"""

websocket_urlpatterns = [
    path('chat/', ChatConsumer),
]

# 在浏览器中输入消息就会通过websocket-->rouging.py-->consumer.py处理后返回给前端
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
            )
        ),
})
