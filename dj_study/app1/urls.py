
from django.urls import path
from .views import *

urlpatterns = [
    path('show_login/',show_login,name='show_login'),
    path('sea_test/',sea_test,name='sea_test'),
    path('upload/',upload,name='upload'),
    path('sea/',sea,name='sea'),
    path('user_info/',user_info,name='user_info'),
]
