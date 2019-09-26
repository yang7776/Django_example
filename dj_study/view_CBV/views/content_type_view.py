# -*- encoding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/9/18 下午10:02
# @Author  : Yang
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from dj_study.view_CBV.models.content_type_model import *
"""
　注意：ContentType只运用于1对多的关系！！！并且多的那张表中有多个ForeignKey字段。
  注意！！！！！！！：
    -  GenericForeignKey("content_type","object_id")  外键ContentType对应的字段名必须是“content_type”，对应的表id字段名必须是“object_id”
"""


def content_type_test(request):
    """
    1、为学位课“python全站”添加一个策略：一个月9.9元
        - 原始做法
            obj = DegreeCourse.objects.get(title="python全站")
            cobj = ContentType.objects.get(model="course")
            PricePolicy.objects.create(price="9.9",period="30",content_type_id=cobj.id,object_id=obj.id)

        - Content_Type做法（快速实现）
            - 注意：content_object(在对应modal中添加此句，不影响表结构) -->  content_object = GenericForeignKey("content_type","object_id")
            obj = DegreeCourse.objects.get(title="python全站")
            PricePolicy.objects.create(price=9.9, period=30, content_object=obj)

    2、根据课程ID获取课程以及对应课程的所有信息
        - 原始做法
            courses = Course.objects.filter(id=1)
            for obj in courses:
                c_info = [
                    obj.id,
                    obj.price,
                    ...
                ]

        - Content_Type做法（反向查找快速实现）
            - 注意：content_object(在对应modal中添加此句，不影响表结构) -->  price_policy_list = GenericRelation("PricePolicy")  PricePolicy为反向查询表名称
            dc_obj = DegreeCourse.objects.get(id=1)
            cd_infos = dc_obj.price_policy_list.all()
            print(cd_infos)

    """
    dc_obj = DegreeCourse.objects.get(id=1)
    cd_infos = dc_obj.price_policy_list.all()
    print(cd_infos)
    return HttpResponse("添加成功")
