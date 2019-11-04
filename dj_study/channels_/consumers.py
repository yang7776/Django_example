# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/11/4 12:02
# file_name     consumers.py
from channels.generic.websocket import WebsocketConsumer    # 文件执行方式为同步
from channels.generic.websocket import AsyncWebsocketConsumer  # 文件执行方式为异步（优化性能）
import json

"""
channel layer主要实现了两种概念抽象：

channel name： channel实际上就是一个发送消息的通道，每个Channel都有一个名称，每一个拥有这个名称的人都可以往Channel里边发送消息

group： 多个channel可以组成一个Group，每个Group都有一个名称，每一个拥有这个名称的人都可以往Group里添加/删除Channel，也可以往
Group里发送消息，Group内的所有channel都可以收到，但是无法发送给Group内的具体某个Channel



这里我们设置了一个固定的房间名作为Group name，所有的消息都会发送到这个Group里边，当然你也可以通过参数的方式将房间名传进来作为Group name，从而建立多个Group，这样可以实现仅同房间内的消息互通

当我们启用了channel layer之后，所有与consumer之间的通信将会变成异步的，所以必须使用async_to_sync

一个链接（channel）创建时，通过group_add将channel添加到Group中，链接关闭通过group_discard将channel从Group中剔除，收到消息时可以调用group_send方法将消息发送到Group，这个Group内所有的channel都可以收的到

group_send中的type指定了消息处理的函数，这里会将消息转给chat_message函数去处理
"""


class ChatConsumer(AsyncWebsocketConsumer):

    # 在连接建立时触发
    async def connect(self):
        self.room_group_name = 'YangRoom'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # 在连接关闭时触发
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 会在收到消息后触发
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',   # 指定消息处理的函数
                'message': message
                }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = '杨先生：' + event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
