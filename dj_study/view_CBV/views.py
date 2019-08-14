from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import *
"""
认证
权限
节流（控制访问频率）
版本
"""
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

##########################################################
import json
from rest_framework.views import APIView
from rest_framework import exceptions
"""
认证：（其实就是将"rest_framework"自带的认证方法源码，取出来以方便自定义用户认证方法）
    注意：以下的所有方法，都可以通过“dispatch”方法寻找的“源码认证流程”
    1、在请求类中执行："authentication_classes"，对应是一个列表，列表中可以放自定义的认证类方法
    2、认证类中的方法，必须执行"authenticate"方法，因为这是源码中的认证方法
    3、在rest_framework中，将原始的request改成了'_request'，所以要利用_request实现取http请求值
    4、规定：返回值为元组类型，第一个值表示user的信息，也可以是user_id，即使用“request.user”获取
"""
# 可以定义一个用户登录认证，其实是把源码中的用户认证方法，提前拿出来使用
class Myauthentication(object):
    def authenticate(self,request):  # 源码中的认证方法，方法中可以自定义用户认证方法
        token = request._request.GET.get("token")  # “_request是原始request”
        if not token:
            raise exceptions.AuthenticationFailed("用户认证失败")
        # restful规定：为了方便后续各个请求视图函数中使用，返回值为元组类型
        # 第一个值取的方法：“request.user”
        # 第二个值取的方法：“request.auth”
        return ("user_info",None)

    def authenticate_header(self,val):  # 配合认证方法的头部信息
        pass

class TestView(APIView):
    authentication_classes = [Myauthentication,]  # 接收请求执行前，先执行认证类

    def get(self,request,*args,**kwargs):
        # self.dispatch()
        print(request.user)
        res = {
            'code':200,
            'user_info':request.user,
            'msg':'test'
        }
        return HttpResponse(json.dumps(res),status=200)

    def post(self,request,*args,**kwargs):
        return HttpResponse('POST')

    def put(self,request,*args,**kwargs):
        return HttpResponse('PUT')

    def delete(self,request,*args,**kwargs):
        return HttpResponse('DELETE')

#############################################################
"""
用户权限：
"""
# 生成随机token值封装
def md5(user):
    import hashlib,time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()

# 用户登录认证
class AuthView(APIView):
    authentication_classes = []
    def post(self,request,*args,**kwargs):
        ret = {'code':1000,'msg':None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = UserInfo.objects.filter(username=user,password=pwd).first()
            if not obj:
                ret["code"] = 1001
                ret["msg"] = '用户名或密码错误'
            # 为登录用户创建token
            token = md5(user)
            # 存在就更新，不存在就创建
            UserToken.objects.update_or_create(user=obj,defaults={'token':token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = "请求异常"
        return JsonResponse(ret)
# 虚拟数据
ORDER_DICT = {
    1:{
        'name':'apple',
        "color":'red',
        'content':'...'
    },
    2: {
        'name': 'orange',
        "color": 'yellow',
        'content': '...'
    }
}
# 定义认证类，和上方相同，定义一个执行http请求前的认证类
"""
注意：此认证可以配置到settings中，成为全局认证方法，即执行任何请求前，都会先执行settings中的"REST_FRAMEWORK"配置的认证类
如果一些请求不需要全局认证，如上方的登录，只需要在请求类中加入“authentication_classes = []”即可。
"""
# class Authentication(object):
#     def authenticate(self,request):
#         token = request._request.GET.get("token")
#         token_obj = UserToken.objects.filter(token=token).first()
#         if not token_obj:
#             raise exceptions.AuthenticationFailed("用户认证失败")
#         return (token_obj.user,token_obj)
#
#     def authenticate_header(self,val):  # 配合认证方法的头部信息
#         pass

# 订单相关业务
class OrderView(APIView):
    # authentication_classes = [Authentication, ]

    def get(self,request,*args,**kwargs):

        # request.user 可取到上方的 ‘token_obj.user’
        # request.auth 可取到上方的 ‘token_obj’
        ret = {'code': 1000, 'msg': None}
        try:
            ret["data"] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)
