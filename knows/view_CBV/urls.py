
from django.urls import path
from .views import *


urlpatterns = [
    path('api/',CbvViews.as_view()),
]
