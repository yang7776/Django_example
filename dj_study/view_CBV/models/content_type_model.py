# -*- encoding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/9/18 下午9:43
# @Author  : Yang
from django.db import models
# ContentType其实是django的内置表，记录了所有自定义表的表名称
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation


class Course(models.Model):
    """
    普通课程
    """
    title = models.CharField(max_length=77)

    class Meta:
        db_table = "ct_course"

class DegreeCourse(models.Model):
    """
    学位课程
    """
    title = models.CharField(max_length=77)

    # Content_Type快速反向查找数据,仅用于反向查找
    price_policy_list = GenericRelation("PricePolicy")

    class Meta:
        db_table = "ct_degreecourse"

class PricePolicy(models.Model):
    """
    价格策略
    """
    price = models.IntegerField()
    period = models.IntegerField()

    content_type = models.ForeignKey(ContentType,verbose_name="关联的表名称",on_delete=None)  # 表名称
    object_id = models.IntegerField(verbose_name="关联的表id")   # 表id

    content_object = GenericForeignKey("content_type","object_id")
    class Meta:
        db_table = "ct_pricepolicy"