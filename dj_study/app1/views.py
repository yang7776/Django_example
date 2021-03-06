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

@csrf_exempt
def upload(request):
    file_obj = request.FILES.get('file')
    id = request.POST.get("id")
    name = request.POST.get("name")
    # photo_format = file_obj.name
    if not file_obj:
        msg = {'code': 401, 'infor': '请上传图片'}
    elif file_obj.name.split('.')[1] not in ['jpg','png','gif']:
        msg = {'code': 400, 'infor': '不支持该类型图片格式'}
    else:
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
    
# Form表单验证bootstrapValidator组件使用
def user_info(request):
    from .forms import UserInfo
    if request.method == "POST":
        user_info_obj = UserInfo(request.POST)   # request.POST为提交过来的所有数据
        if not user_info_obj.is_valid():    # is_valid判断输入的内容是否合法 Ture 或False
            for k, err in user_info_obj.errors.items(): # for循环找出错误
                return HttpResponse(json.dumps({"code":400,"msg": "错误参数：{}，错误原因：{}".format(k,err)}))   # 返回错误信息

        # clean()获取提交的数据，这个函数主要作用是单独拿出来一些数据再次效验
        # 因为forms类中的一些效验是没有逻辑的，如果需要一些逻辑性效验或者字段联系性效验，就需要单独拿出来效验
        info = user_info_obj.clean()
        username = info.get("username")
        if int(username) % 7 != 0 :
            return HttpResponse(json.dumps({"code":401,"msg": "用户名ID必须是7的倍数"}))  # 返回错误信息
        iphone = info.get("iphone")
        User_Iphone.objects.create(username=username, iphone=iphone)
        return HttpResponse(json.dumps({"code":200,"msg": "创建成功"}))
    return render(request,'from_validate.html')   # 无论有没有数据，渲染页面