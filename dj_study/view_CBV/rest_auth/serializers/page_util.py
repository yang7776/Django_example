# -*- encoding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/9/17 下午8:44
# @Author  : Yang
from rest_framework import serializers
from dj_study.view_CBV.models.rest_model2 import Role
class PagerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
