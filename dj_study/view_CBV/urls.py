
from django.urls import path,re_path,include
from dj_study.view_CBV.views.rest_view1 import *
from dj_study.view_CBV.views.rest_view2 import *
from dj_study.view_CBV.views.content_type_view import *

# 自动生成路由
from rest_framework import routers
router = routers.DefaultRouter()  # 实例化路由对象
router.register(r"auto_url",View2View)  # 注册路由对象，自动生成四种类型url（获取全部数据，基本增删改查，format参数，format+增删改查）

urlpatterns = [

    #################rest_url2#################################

    # 简单restful请求
    path('rest_ful1/',CbvViews.as_view()),
    # restful 用户权限
    path('rest_ful3/v1/auth/',AuthView.as_view()),
    path('rest_ful3/v1/order/',OrderView.as_view()),

    #################rest_url2#################################

    # 版本
    re_path('(?P<version>[v1|v2|v3]+)/users/$',UsersView.as_view(),name="user"),  # 注意使用“re_path”

    # 解析器
    re_path('(?P<version>[v1|v2|v3]+)/analyze/$',AnalyzeView.as_view(),name="analyze"),

    # 序列化(功能一：数据序列化)
    re_path('(?P<version>[v1|v2|v3]+)/roles/$',RoleView.as_view(),name="roles"),
    re_path('(?P<version>[v1|v2|v3]+)/userinfo/$',UserInfoView.as_view(),name="userinfo"),
    re_path('(?P<version>[v1|v2|v3]+)/group/(?P<gid>\d+)$',GroupView.as_view(),name="group"),
    # 序列化(功能二：数据校验)
    re_path('(?P<version>[v1|v2|v3]+)/usergroup/$',UserGroupView.as_view(),name="usergroup"),

    # 分页
    re_path('(?P<version>[v1|v2|v3]+)/page1/$',Page1View.as_view()),

    # 视图
    re_path('(?P<version>[v1|v2|v3]+)/view1/$',View1View.as_view()),
    # put:全部更新  patch：局部更新  "get":"retrieve"获取一条数据（list是获取全部数据）
    # http://127.0.0.1:8000/view_cbv/v3/view2/   # 查看全部数据
    re_path('(?P<version>[v1|v2|v3]+)/view2/$',View2View.as_view({"get":"list"})),
    # http://127.0.0.1:8000/view_cbv/v3/view2.json
    re_path('(?P<version>[v1|v2|v3]+)/view2\.(?P<format>\w+)$',View2View.as_view({"get":"list"})),
    # http://127.0.0.1:8000/view_cbv/v3/1/    查询id为1的数据
    re_path('(?P<version>[v1|v2|v3]+)/view2/(?P<pk>\d+)/$',View2View.as_view({
        "get":"retrieve",
        "post":"create",
        "put":"update",
        "patch":"partial_update",
        "delete":"destroy",
    })),

    # 路由（配置后自动生成四种url）
    # http://127.0.0.1:8000/view_cbv/v3/auto_url.json
    re_path('(?P<version>[v1|v2|v3]+)/',include(router.urls)),

    # 渲染器
    re_path('(?P<version>[v1|v2|v3]+)/view3/$',View3View.as_view()),

    # Content_Type
    path('content_type_test/',content_type_test),
]
