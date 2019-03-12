from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json,os
from .models import Person,SeaTest
from django.conf import settings

# Create your views here.
def show_login(request):
    pers = Person.objects.all()
    return render(request,"login.html",{"pers":pers})

def sea_test(request):
    ajax_url = '/app1/sea/'
    return render(request,"sea_test.html",{"ajax_url":ajax_url})

@csrf_exempt
def upload(request):
    file_obj = request.FILES.get('file')
    id = request.POST.get("id")
    name = request.POST.get("name")
    Person.objects.create(selfid=id, name=name,photo=file_obj)
    msg = {'code': 200,'infor': '注册成功'}
    return HttpResponse(json.dumps(msg))

def sea(request):
    # 分页数据
    offset = int(request.GET.get("iDisplayStart", 0))
    limit = int(request.GET.get("iDisplayLength", 10))
    id = request.GET.get('id',"")
    name = request.GET.get('name',"")
    sex = request.GET.get('sex',"")
    age = request.GET.get('age',"")
    # sea_type = request.GET.get('search_type')   # 接收的“查询类型”
    # sea_res = request.GET.get('search_res',"")   # 根据查询类型找到对应数据
    sEcho = request.GET.get('sEcho')
    data_info = []
    sea_items = {}
    if id:
        sea_items.update({'id':int(id)})
    if name:
        sea_items.update({'name': name})
    if sex:
        sea_items.update({'sex': sex})
    if age:
        sea_items.update({'age': int(age)})
    items = SeaTest.objects.filter(**sea_items)
    total = items.count()
    items = items[offset:offset + limit]
    for item in items:
        per = [
            item.id,
            item.sex,
            item.age,
            item.name,
            str(item.id) + " | " + item.name,
            ""
        ]
        data_info.append(per)
    return HttpResponse(json.dumps({
        "data": {
            "data_list": data_info,
            "iTotalRecords": total,
            "iTotalDisplayRecords": total,
            "sEcho": sEcho
        }
    }))
