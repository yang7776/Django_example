"""knows URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *


urlpatterns = [
    path('select/',select),
    path("sel/",sel,name='sel'),
    path("cache/",cache_test,name='cache_t'),
    path("test_item/",test_item),
    path("teacher_test/",teacher_test,name="teacher_test"),
    path("teacher_test_update/",teacher_test_update,name="teacher_test_update"),
]
