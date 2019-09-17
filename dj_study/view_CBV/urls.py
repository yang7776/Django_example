
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
    # http://127.0.0.1:8000/view_cbv/v3/view2/3/
    re_path('(?P<version>[v1|v2|v3]+)/view2/$',View2View.as_view({"get":"list"})),
    re_path('(?P<version>[v1|v2|v3]+)/view2/(?P<pk>\d+)/$',View2View.as_view({
        "get":"retrieve",
        "post":"create",
        "put":"update",
        "patch":"partial_update",
        "delete":"destroy",
    })),
    # re_path('(?P<version>[v1|v2|v3]+)/view2/',View2View.as_view({"get":"list","post":"post_list"})),
]
