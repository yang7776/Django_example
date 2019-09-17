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
序列化有以下两种功能：
    - 数据序列化，有以下三种方式：
        - 简单序列化，正常定义
        - rest自带类"Serializer"进行序列化转换，自定义输出方式
        - rest自带类"ModelSerializer"进行序列化转换，可直接输出全部字段，因为继承方式二类，所以也可自定义输出方式和扩展字段参数（即方式二同样适用），或者改变原有字段参数（extra_kwargs）
    - 数据校验：
        - 普通的判断如“字段是否为空”，可直接校验error_messages={"required":"标题不能为空"}
        - 一些字段需要自定义校验，可自定义校验类validators=[CustomValid("七")]
"""
##########################################序列化功能一：数据序列化################################################
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

# 单独定义某个字段的url
class LinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInfoT
        # HyperlinkedModelSerializer 会自动生成一个 url 字段来表示超链接
        # 我们希望 API 中包括这个字段，所以这里我们在 fields 加上
        fields = ["id","username","password","user_type","group"]

        # 我们可以在 extra_kwargs 设置中的 view_name 和 lookup_field
        # 来正确配置我们的 URL
        # view_name 和 urls.py 中的 name 参数相对应，表示使用哪个 url
        # lookup_field 表示用哪个字段来作为 url 的唯一识别标记
        # 本例中每个 Profile 的 url 是通过 id 来区分的，所以该字段用 id
        extra_kwargs = {
            'group': {'view_name': 'group', 'lookup_field': 'id','lookup_url_kwarg':'gid'},
        }

class UserInfoSerializerT(serializers.ModelSerializer):
    group = serializers.HyperlinkedIdentityField(view_name='group',lookup_field='group_id',lookup_url_kwarg='gid')  # 反向生成url，点击可以查看对应资源
    class Meta:
        model = UserInfoT

        # fields = "__all__"  # 表示输出全部字段数据
        fields = ["id","username","password","user_type","group"]  # 只输出指定字段
        depth = 1  # 深度取值，1即表示，判断取的字段中，是否有往下一层可取的值（如一对多，多对多等关联表），若有输出下一层的值（即自动联表取值）。注意：深度取值也意味着值越大，深度层数越多，即会影响取值效率，官网建议“0~10”之间。

        extra_kwargs = {
            'username':{'min_length':50},
        }  # 可以使用extra_kwargs参数为ModelSerializer添加或修改原有的选项参数

class UserInfoView(CancelRest1Class,APIView):
    def get(self,request,*args,**kwargs):

        users = UserInfoT.objects.all()
        # context={'request': request}：需要字段反向生成url时，需要设置此字段
        # 以下方式一和方式二，方式一推荐字段中“link字段”多的时候，方式二适合没有“link字段”的时候
        """
        源码流程：
            1.实例化，将参数传递的数据封装到对象，指向"__new__()"<根据many的真假，确定返回的对象>返回的对象
            2.调用对象的data属性
        """
        ser = LinkSerializer(instance=users,many=True,context={'request': request})   # 方式一：使用获取“字段link”的类，来获取所需的所有字段
        # ser = UserInfoSerializerT(instance=users,many=True,context={'request': request})  # 方式二：使用获取“字段”的类，来获取所需的所有字段，link字段再使用HyperlinkedIdentityField获取
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

class GroupView(CancelRest1Class,APIView):
    def get(self, request, *args, **kwargs):
        gid = kwargs.get("gid")
        group = UserGroup.objects.get(id=gid)
        data = {"id":group.id,"title":group.title}
        ret = json.dumps(data,ensure_ascii=False)
        return HttpResponse(ret)

##########################################序列化功能二：数据校验################################################
# 自定义验证类
class CustomValid(object):
    def __init__(self,base):
        self.base = base

    def __call__(self, value):  # 当执行字段校验的时候，就会执行__call__函数,value为用户传来的值
        """
        序列化自定义验证类时用法：
            __call__() 方法中来构造更复杂或者可配置的验证器，这个方法相当于一个纯粹的函数式“自定义校验类”的调用
        普通用法：
            __call__: 改变实体的位置，当传入的值符合__call__对应的参数时，就是执行__call__，而不执行__init__。
        """
        if not value.startswith(self.base):
            err_msg = "标题必须以%s为开头"%self.base
            raise serializers.ValidationError(err_msg)

    def set_context(self,serializer_field):
        """
        执行验证之前调用，serializer_field为当前字段对象
        """
        print("执行验证之前调用")

class UserGroupSerializer(serializers.Serializer):
    # 定义字段，并设置对应校验
    title = serializers.CharField(error_messages={"required":"标题不能为空"},validators=[CustomValid("七"),])

class UserGroupView(CancelRest1Class,APIView):
    def post(self, request, *args, **kwargs):

        ser = UserGroupSerializer(data=request.data)  # 定义的序列化类
        if ser.is_valid():
            print(ser.validated_data)  # 验证通过时，输出title对象
            # print(ser.validated_data["title"])  # 验证通过时，输出title值，可以将值拿出来
        else:
            print(ser.errors)   # 输出错误对象
            # print(ser.errors["title"][0])    # 输出对应的错误信息”标题不能为空“

        return HttpResponse("提交数据")

# TODO：分页
"""
分页类型
    - 类型一：看第n页，每页显示n条数据
    - 类型二：在n个位置，向后查看n条数据
    - 类型三：加密分页，只能看上一页和下一页。一次只读取一页的值，速度快（适用于数据量大）
"""
from dj_study.view_CBV.rest_auth.serializers.page_util import PagerSerialiser  # 引入文件自定义的序列化类
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination
from rest_framework.response import Response  # 数据渲染类

# 分页类型一
class MyPageNumberPagination(PageNumberPagination):
    # http://127.0.0.1:8000/view_cbv/v3/page1/?page=3&size=4  读取第3页的4条数据
    page_size = 2   # 一页显示多少个
    page_query_param = "page"  # 获取页码的key
    page_size_query_param = "size"  # 设置在url中还可以”再设置“一页显示数，key值为size
    max_page_size = 5   # 每页显示最多几条数据

# 分页类型二
class MyLimitOffsetPagination(LimitOffsetPagination):
    # http://127.0.0.1:8000/view_cbv/v3/page1/?offset=0&limit=4  从索引0开始读取4条数据
    default_limit = 2  # 默认读取多少条数据
    offset_query_param = 'offset'  # 获取从数据索引几开始读的key
    limit_query_param = 'limit'    # 获取从数据索引几读多少条数据的key
    max_limit = 5                  # 最多读取多少条数据

# 分页类型三
class MyCursorPagination(CursorPagination):
    # http://127.0.0.1:8000/view_cbv/v3/page1/?size=4   注意使用“get_paginated_response”来返回，才可看到上一页和下一页的链接
    cursor_query_param = 'cursor'  # 翻页时的key，注意这个key是随机生成，不知道页码，即需要get_paginated_response来显示上一页和下一页的链接
    ordering = 'id'   # 根据指定字段排序，注意“-+字段名”是降序，直接写“字段名”是升序
    page_size = 2  # 一页显示多少条数据
    page_size_query_param = "size"  # 设置在url中还可以”再设置“一页显示数，key值为size
    max_page_size = 5  # 每页显示最多几条数据

class Page1View(CancelRest1Class,APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = Role.objects.all()

        # 创建分页对象
        # pg = PageNumberPagination()   # 用此内置的分页类，需要在settings中配置”PAGE_SIZE“,即每页显示数。
        # pg = MyPageNumberPagination()   # 自定义分页类，继承专用类后，可灵活修改参数
        # pg = MyLimitOffsetPagination()  # 自定义索引分页类，继承专用类后，可灵活修改参数
        pg = MyCursorPagination()         # 自定义加密分页类，继承专用类后，可灵活修改参数

        # 在数据库中获取分页的数据（返回的是数据modal对象）
        page_role = pg.paginate_queryset(queryset=roles,request=request,view=self)

        # 对数据进行序列化
        ser = PagerSerialiser(instance=page_role, many=True)

        # 通过get_paginated_response方法返回分页的详细信息和数据
        get_page_response = pg.get_paginated_response(ser.data)
        return get_page_response  #　不仅返回对应数据，也返回数据总数，下一页和上一页的链接(加密分页需要)等
        # return Response(ser.data)   # 直接返回对应页数的数据

# TODO：视图
"""
视图有两个类：
    - GenericAPIView：相当于将上方的分页，序列化等封装成一个类，直接用已经封装好的一些方法（适合复杂性逻辑）
    - GenericViewSet：注意此时路由也有对应变化，{“get”:"list"}即是get请求对应的是”list“方法，并可以单独继承增删改查其中的一个或多个方法（灵活）
    - ModelViewSet：最强大的类，自带“基本”数据增删该查，注重“url配置,一般配置两个url，一个访问全部数据，一个增删改查（根据需求）”
注意：在使用此视图时，可配置“权限”，此权限是指对“数据对象”访问的权限：
    GenericAPIView.get_object
        check_object_permissions.has_object_permission(之前的是“has_permission”,是指对所有数据的权限)
"""
from rest_framework.generics import GenericAPIView
class View1View(CancelRest1Class,GenericAPIView):
    # 提前定义需要用的类对象
    queryset = Role.objects.all()
    serializer_class = PagerSerialiser
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()  # 获取上方定义的 queryset
        # 分页
        page_roles = self.paginate_queryset(roles)   # 获取上方定义的 PagerSerialiser
        # 序列化
        ser = self.get_serializer(instance=page_roles,many=True)  # 获取上方定义的 PageNumberPagination

        return Response(ser.data)

# 继承ModelViewSet后，只需要明确数据对象即可
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin # 增加，删除类方法，ModelViewSet都包含
from rest_framework.viewsets import ModelViewSet  # ModelViewSet继承了数据的增删改查功能，以及GenericViewSet功能
# class View2View(CancelRest1Class,CreateModelMixin,ModelViewSet):  # 也可以单独只定义视图增加功能
class View2View(CancelRest1Class,ModelViewSet):
    # 提前定义需要用的类对象
    queryset = Role.objects.all()  # 获取全部数据对象
    serializer_class = PagerSerialiser  # 获取序列化对象
    pagination_class = PageNumberPagination  # 获取分页对象