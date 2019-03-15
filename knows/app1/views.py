from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json,os
from .models import Person,SeaTest,User_Iphone
from django.conf import settings

# Create your views here.
def show_login(request):
    pers = Person.objects.all()
    return render(request,"login.html",{"pers":pers})

# datatable.js组件使用
def sea_test(request):
    ajax_url = '/app1/sea/'
    return render(request,"sea_test.html",{"ajax_url":ajax_url})

# Form表单验证bootstrapValidator组件使用
def form_val(request):
    return render(request,"from_validate.html")

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
    items = SeaTest.objects.filter(**sea_items).order_by("age")  # order_by()：可以根据指定字段排序
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
    
# Django自带form组件
def user_info(request):
    from .forms import UserInfo
    obj = UserInfo()   # 创建form对象
    if request.method == "POST":
        user_info_obj = UserInfo(request.POST)   # request.POST为提交过来的所有数据
        if user_info_obj.is_valid():    # is_valid判断输入的内容是否合法 Ture 或False
            info = user_info_obj.clean()    # clean()获取提交的数据
            # 以下是以“GET”方法去处理get接收的数据，并通过HttpResponseRedirect发给指定的views函数
            b = ""
            for k,v in info.items():
                a = "&{}={}".format(k,v)
                b = a + b
            return HttpResponseRedirect('/app1/create_user/?%s'%b)
        else:
            error_msg = user_info_obj.errors
            return render(request,"from_validate.html",{'errors':"用户名超过三个字符"})
    return render(request,'from_validate.html',{'msg':"请求方式错误"})

def create_user(request):
    username = request.GET.get("username")
    iphone = request.GET.get("iphone")
    print(username,iphone)
    User_Iphone.objects.create(username=username,iphone=iphone)
    return HttpResponse(json.dumps({"msg":"创建成功"}))