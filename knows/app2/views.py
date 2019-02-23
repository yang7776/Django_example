from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# 全站缓存时，设置指定视图忽略缓存
from django.views.decorators.cache import never_cache
# 非全站缓存时，设置指定视图缓存多长时间
from django.views.decorators.cache import cache_page


import json,os
import logging
# 生成一个以当前文件名为名字的logger实例
# logger = logging.getLogger("django")
# 生成一个名为collect的logger实例
# collect_logger = logging.getLogger("collect")

# Create your views here.
def select(request):
    return render(request,"select.html")
    
def test_item(request):
    tests = Test_item.objects.all()
    return render(request,"test_teacher_item.html",locals())

@cache_page(7) # 设置该视图缓存7秒
def cache_test(request):
    teas = Teacher.objects.all()
    stus = Student.objects.all()
    majors = Major.objects.all()
    return render(request,"cache_test.html",locals())

@csrf_exempt
def sel(request):
    id = request.POST.get('tid')   # 前端传值为777
    aid = request.POST.get('aid')
    bid = request.POST.get('bid')
    print(aid)
    print(bid)
    # ses = request.session.values()
    if request.session.get('id') == id:
        return HttpResponse("ID已被申请")
    else:
        request.session['id'] = id
    return HttpResponse("ID申请成功")

@csrf_exempt
def teacher_test(request):
    id = request.POST.get('id')   # 前端传值为7
    name = request.POST.get('name')
    data = {
        "test_id":id,
        "test_name":name
    }
    Test_item.objects.create(**data)
    return HttpResponse(json.dumps({"msg":"创建成功"}))\
    
@csrf_exempt
def teacher_test_update(request):
    id = request.POST.get('id')   # 前端传值为7
    name = request.POST.get('name')
    obj = Test_item.objects.filter(test_id=id).exists()  # 判断对应数据实例是否存在
    if not obj:
        return HttpResponse(json.dumps({"msg": "无对象"}))
    else:
        test_id_compare = Test_item.objects.judge_id(id)  # 调用此表格中的Manager函数，即调用此表格的一个方法
        print(test_id_compare)  # 输出对应方法的返回值,并在下方返回到前端
        objs = Test_item.objects.get(test_id=id)
        objs.test_name = name
        objs.save()
        return HttpResponse(json.dumps({"msg":"更改成功","test_id_compare":test_id_compare}))

