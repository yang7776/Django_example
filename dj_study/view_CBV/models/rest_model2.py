# -*- encoding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/9/8 下午5:12
# @Author  : Yang
from django.db import models
user_type_choices = (
    (1,'普通用户'),
    (2,'vip'),
    (3,'SVIP'),
)
class UserGroup(models.Model):
    title = models.CharField(max_length=77)
    class Meta:
        db_table = "rest2_usergroup"


class Role(models.Model):
    title = models.CharField(max_length=77)
    class Meta:
        db_table = "rest2_role"


class UserInfoT(models.Model):
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=77,unique=True)
    password = models.CharField(max_length=77)
    group = models.ForeignKey("UserGroup",on_delete=None)
    roles = models.ManyToManyField("Role")
    class Meta:
        db_table = "rest2_userinfo"

class UserTokenT(models.Model):
    user = models.OneToOneField(to='UserInfo',on_delete=None)
    token = models.CharField(max_length=77)
    class Meta:
        db_table = "rest2_usertoken"