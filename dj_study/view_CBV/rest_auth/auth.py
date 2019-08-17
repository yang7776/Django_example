# -*- encoding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/8/13 下午9:56
# @Author  : Yang

from dj_study.view_CBV.models import *
from rest_framework import exceptions
# 定义认证类，和上方相同，定义一个执行http请求前的认证类
class FirstAuthentication(object):
    def authenticate(self,request):
        pass

    def authenticate_header(self,val):  # 配合认证方法的头部信息
        pass

class Authentication(object):
    def authenticate(self,request):
        token = request._request.GET.get("token")
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        return (token_obj.user,token_obj)

    def authenticate_header(self,val):  # 配合认证方法的头部信息
        pass