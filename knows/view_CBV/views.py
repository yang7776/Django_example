from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# 若需要给多个CBV视图同时加上一个方法，我们就需要改变父类中的“dispatch”方法，并让对应视图类继承即可
class Common(object):
    def dispatch(self,request,*args,**kwargs):
        print("执行method方法之前")
        res = super(Common,self).dispatch(request,*args,**kwargs)
        print("执行method方法之后")
        return res

@method_decorator(csrf_exempt,name='dispatch')  # CBV中csrf验证方法，和FBV不同
class CbvViews(Common,View):
    def get(self,request,*args,**kwargs):
        print("执行get方式的视图方法")
        return HttpResponse('GET')

    def post(self,request,*args,**kwargs):
        return HttpResponse('POST')

    def put(self,request,*args,**kwargs):
        return HttpResponse('PUT')

    def delete(self,request,*args,**kwargs):
        return HttpResponse('DELETE')