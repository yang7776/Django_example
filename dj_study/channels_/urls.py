# -*- coding: utf-8 -*-
from django.urls import path
from dj_study.channels_.views import chat

urlpatterns = [
    path('chat', chat, name='chat-url')
]