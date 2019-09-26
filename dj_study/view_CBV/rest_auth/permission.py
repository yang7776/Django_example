# -*- encoding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/8/18 下午4:42
# @Author  : Yang

# 权限类方法

from rest_framework.permissions import BasePermission
# 规范性：继承BasePermission


class SvipPermission(BasePermission):

    # 规定权限类，user_type为3才可以访问对应资源
    def has_permission(self, request, view):  # restful源码方法，优先执行
        if request.user.user_type != 3:
            return False  # 认证失败
        return True       # 认证成功
