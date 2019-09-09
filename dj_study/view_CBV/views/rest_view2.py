# -*- encoding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2019/9/8 下午5:34
# @Author  : Yang
import json
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from dj_study.view_CBV.models.rest_model2 import *
from rest_framework.request import Request
from dj_study.view_CBV.rest_auth.throttle import UserThrottle
"""
1、版本(*)
2、解析器(*)
3、序列化(***)
    1.请求数据进行校验（django-form也可以校验）
    2.QuerySet进行序列化
4、分页(**)
5、路由(**)
6、视图(**)
7、渲染器(*)
"""
class CancelRest1Class(object):
    # 全局定义类
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

#TODO：版本相关
"""
版本：有以下六种方式，推荐第三种方法，嵌套在url中。在settings中配置相关参数，如默认版本号等，可在settings中配置为全局获取方法。注意全局配置时，指定的不是列表，而是字符串。
    - 普通方法，版本可以通过url“GET”传参
    - 利用rest自带的版本方法类QueryParameterVersioning，通过GET传参获取
    - 推荐方法：将版本号嵌套在url链接中，使用URLPathVersioning方法类获取版本号，url配置中设置为正则。
    - AcceptHeaderVersioning：基于请求头来指定对应的版本
    - NamespaceVersioning：基于url中的name_space来指定对应的版本
    - HostNameVersioning：基于子域名来指定对应的版本
"""
from rest_framework.versioning import BaseVersioning  # 获取版本信息的类
from rest_framework.versioning import QueryParameterVersioning  # rest中版本类，在get传递的参数中取值
from rest_framework.versioning import URLPathVersioning  # rest版本类，在url中取值，即是将版本号嵌套在url链接中
class ParamVersion(object):
    # 获取version版本值，若需要扩展的话，可以使用此方法自定义，即自定义类后，使用一下函数
    def determine_version(self, request, *args, **kwargs):  # 内部定义好的方法，获取版本信息
        version = request.query_params.get("version") # query_params获取版本信息
        return version

class UsersView(CancelRest1Class,APIView):
    # 版本类
    # versioning_class = QueryParameterVersioning  # 获取版本类信息(GET传参)
    # versioning_class = URLPathVersioning  # 获取版本类信息(url嵌套版本号),可在setting中设置为全局

    def get(self,request,*args,**kwargs):
        print(request.version)  # 输出版本号
        print(request.versioning_scheme)  # 输出版本对象
        print(request.versioning_scheme.reverse(viewname="user",request=request))   # 输出“反向生成对应的url”(注意在url配置中，设置“name”参数)
        return HttpResponse('用户列表')

# TODO：解析器相关
"""
相关注意：
请求头要求：以下两个要求都满足，request.post才能取到值，如果其中有一个或两个不满足可从“request.body”获取数据，因为request.body会接收所有类型值。
    - Content-Type = application/x-www-form-urlencoded
    - 数据格式：  name=xiaoqi&age=17 (接收的格式化数据，非json)
"""
from rest_framework.parsers import JSONParser  # 允许前端发送json数据
from rest_framework.parsers import FormParser  # 允许前端发送form表单数据
class AnalyzeView(CancelRest1Class,APIView):
    parser_classes = [JSONParser,FormParser]  # 可以导入解析器类直接使用或全局设置
    """
    parser_classes：也可以进行全局配置
    JSONParser：只能解析Content-Type = application/json头的数据
    FormParser：只能解析Content-Type = application/application/x-www-form-urlencoded头的数据
    MultiPartParser：只能解析请求头content-type = multipart/form-data的请求体的数据，是form表单的上传文件
    FileUploadParser：可以解析全部格式，一般多用于上传文件
    """
    def post(self,request,*args,**kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """
        1、获取用户请求
        2、获取用户请求体
        3、根据用户请求头和“parser_classes”中支持的的请求头进行比较
        4、交给符合的对象，如JSONParser，去处理请求体中的数据
        5、将处理之后的数据赋值给request.data
        """

        print(request.data)  # 获取解析后的数据，接收的直接就是json解析后的数据
        return HttpResponse('request.post/request.body')

# TODO：序列化
"""
序列化有以下三种方式：
    - 简单序列化，正常定义
    - rest自带类"Serializer"进行序列化转换，自定义输出方式
    - rest自带类"ModelSerializer"进行序列化转换，可直接输出全部字段，因为继承方式二类，所以也可自定义输出方式和扩展字段参数（即方式二同样适用），或者改变原有字段参数（extra_kwargs）
"""
from rest_framework import serializers
class RoleSerializer(serializers.Serializer):
    title = serializers.CharField()  # 将指定字段序列化，注意“字段”必须是数据表中的字段，在这里不能自定义
    id = serializers.CharField()
class RoleView(CancelRest1Class,APIView):
    def get(self,request,*args,**kwargs):

        # # 方式一：简单序列化
        # roles = Role.objects.values("id","title")
        # roles = list(roles)
        # ret = json.dumps(roles,ensure_ascii=False)

        # 方式二：rest自带类"serializers"进行序列化转换
        roles = Role.objects.values("id", "title")
        ser = RoleSerializer(instance=roles,many=True)  # instance:序列化Queryset列表，many：指定实例化Queryset列表中有多个对象时，指定为True；若为一个对象，必须many设为False
        ret = json.dumps(ser.data, ensure_ascii=False)  # ser.data：为序列化之后的结果，ensure_ascii：默认为True，是否为输出的结果进行转码，若不设置为False，用网页访问时，返回的数据为“中文”转码后的数据
        return HttpResponse(ret)

# 方式二：下面为使用自定义序列化类展示的所有类型的数据序列化，如一对多，多对多等，适合需要自定义返回值时使用。
class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    u_type = serializers.CharField(source="get_user_type_display")  # source：相当于<UserInfoT>.get_user_type_display
    u_group = serializers.CharField(source="group.id")  # 一对多外键可用
    u_roles = serializers.SerializerMethodField()  # 自定义显示，一般用于多对多
    def get_u_roles(self,row): # 注意：多对多自定义返回值的方法名，必须是“get+对应字段名”
        role_obj_list = row.roles.all().values_list("title",flat=True)
        return list(role_obj_list)

# 方式三，直接返回对应表里的所有数据，将所有数据序列化，不用一个一个写,并且可以扩展自定义字段输出方式
class MyField(serializers.CharField):  # 可以自定义类返回字段（不常用）
    def to_representation(self, value):
        return value   # value；就是调用该类指定字段的返回值
class UserInfoSerializerT(serializers.ModelSerializer):
    group = serializers.HyperlinkedIdentityField(view_name='group',lookup_field='group_id',lookup_url_kwarg='gid')  # 反向生成url，点击可以查看对应资源
    class Meta:
        model = UserInfoT

        # fields = "__all__"  # 表示输出全部字段数据
        fields = ["id","username","password","user_type","group"]  # 只输出指定字段
        depth = 1  # 深度取值，1即表示，判断取的字段中，是否有往下一层可取的值（如一对多，多对多等关联表），若有输出下一层的值（即自动联表取值）。注意：深度取值也意味着值越大，深度层数越多，即会影响取值效率，官网建议“0~10”之间。

        extra_kwargs = {'username':{'max_length':50}}  # 可以使用extra_kwargs参数为ModelSerializer添加或修改原有的选项参数
class UserInfoView(CancelRest1Class,APIView):
    def get(self,request,*args,**kwargs):

        users = UserInfoT.objects.all()
        # context={'request': request}：需要字段反向生成url时，需要设置此字段
        ser = UserInfoSerializerT(instance=users,many=True,context={'request': request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

class GroupView(CancelRest1Class,APIView):
    def get(self, request, *args, **kwargs):
        gid = kwargs.get("gid")
        group = UserGroup.objects.get(id=gid)
        data = {"id":group.id,"title":group.title}
        ret = json.dumps(data,ensure_ascii=False)
        return HttpResponse(ret)