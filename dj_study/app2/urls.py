
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
