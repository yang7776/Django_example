
from django.urls import path,re_path
from dj_study.view_CBV.views.rest_view1 import *
from dj_study.view_CBV.views.rest_view2 import *


urlpatterns = [

    #################rest_url2#################################

    # 简单restful请求
    path('rest_ful1/',CbvViews.as_view()),
    # restful 用户权限
    path('rest_ful3/v1/auth/',AuthView.as_view()),
    path('rest_ful3/v1/order/',OrderView.as_view()),

    #################rest_url2#################################

    # 版本
    re_path('(?P<version>[v1|v2|v3]+)/users/',UsersView.as_view(),name="user"),  # 注意使用“re_path”

    # 解析器
    re_path('(?P<version>[v1|v2|v3]+)/analyze/',AnalyzeView.as_view(),name="analyze"),

    # 序列化
    re_path('(?P<version>[v1|v2|v3]+)/roles/',RoleView.as_view(),name="roles"),
    re_path('(?P<version>[v1|v2|v3]+)/userinfo/',UserInfoView.as_view(),name="userinfo"),
    re_path('(?P<version>[v1|v2|v3]+)/group/(?P<gid>\d+)$',GroupView.as_view(),name="group"),
]
