# -*- encoding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/8/13 下午9:56
# @Author  : Yang

# 认证类方法

from dj_study.view_CBV.models.rest_model1 import *
from rest_framework import exceptions
# 认证类，必须继承“BaseAuthentication”
from rest_framework.authentication import BaseAuthentication
# 定义认证类，和上方相同，定义一个执行http请求前的认证类
class FirstAuthentication(BaseAuthentication):
    def authenticate(self,request):
        pass

    def authenticate_header(self,val):  # 配合认证方法的头部信息
        pass

class Authentication(BaseAuthentication):
    def authenticate(self,request):
        token = request._request.GET.get("token")
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        return (token_obj.user,token_obj)   # 规定返回必须是元组类型

    def authenticate_header(self,val):  # 配合认证方法的头部信息
        pass