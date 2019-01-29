from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json,os
import logging
# 生成一个以当前文件名为名字的logger实例
# logger = logging.getLogger("django")
# 生成一个名为collect的logger实例
# collect_logger = logging.getLogger("collect")


# Create your views here.
def select(request):
    return render(request,"select.html")

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

