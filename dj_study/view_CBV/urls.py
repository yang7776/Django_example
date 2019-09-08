
from django.urls import path
from dj_study.view_CBV.views.rest_view1 import *


urlpatterns = [
    # 简单restful请求
    path('rest_ful1/',CbvViews.as_view()),
    # restful 用户权限
    path('rest_ful3/v1/auth/',AuthView.as_view()),
    path('rest_ful3/v1/order/',OrderView.as_view()),

]
