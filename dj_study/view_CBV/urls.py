
from django.urls import path
from view_CBV.views import *


urlpatterns = [
    # 简单restful请求
    path('rest_ful1/',CbvViews.as_view()),
    # restful 用户认证
    path('rest_ful2/',TestView.as_view()),
    # restful 用户权限
    path('rest_ful3/v1/auth/',AuthView.as_view()),
    path('rest_ful3/v1/order/',OrderView.as_view()),

]
