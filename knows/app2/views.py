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

