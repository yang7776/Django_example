from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json,os
from .models import Person
from django.conf import settings

# Create your views here.
def show_login(request):
    pers = Person.objects.all()
    return render(request,"login.html",{"pers":pers})

@csrf_exempt
def upload(request):
    file_obj = request.FILES.get('file')
    id = request.POST.get("id")
    name = request.POST.get("name")
    Person.objects.create(selfid=id, name=name,photo=file_obj)
    msg = {'code': 200,'infor': '注册成功'}
    return HttpResponse(json.dumps(msg))
