
from django.urls import path,re_path
from dj_study.dwebsocket_.views import *

urlpatterns = [
    re_path(r'^ws_chat/(?P<userid>[0-9]+)$', ws_chat, name='ws_chat'),
]
