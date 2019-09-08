from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dj_study.view_CBV.models.rest_model1 import *
from rest_framework.views import APIView
from dj_study.view_CBV.rest_auth.throttle import UserThrottle

"""
简单restful使用：（其实就是将"rest_framework"自带的认证方法源码，取出来以方便自定义用户认证方法）
    注意：以下的所有方法，都可以通过“dispatch”方法寻找的“源码认证流程”
    1、在请求类中执行："authentication_classes"，对应是一个列表，列表中可以放自定义的认证类方法
    2、在rest_framework中，将原始的request改成了'_request'，所以要利用_request实现取http请求值
    3、规定：返回值为元组类型，第一个值表示user的信息，也可以是user_id，即使用“request.user”获取
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

#############################################################
"""
认证：
    1、重新创建文件夹，自定义认证类，注意必须继承“BaseAuthentication”这个类：from rest_framework.authentication import BaseAuthentication
    2、全局配置认证类，在setttings中配置“REST_FRAMEWORK”，可以认证登录，输出匿名用户的值等，成为全局认证方法后，即执行任何请求前，都会先执行settings中的"REST_FRAMEWORK"配置的认证类,
    3、全局配置后，不需要认证的方法，可以在对应方法中加入“authentication_classes = []”,认证类中的方法，必须先执行"authenticate"方法，因为这是源码中的认证方法
    4、认证成功后返回值规定：返回值为元组类型，第一个值表示user的信息，也可以是user_id，即使用“request.user”获取，第二个值表示相关认证信息，使用“request.auth”获取
    4、没有登录的用户，即匿名用户，访问资源时，对应的“request.user”默认等于“AnonymousUser”(可以拿此做一些判断)，但当在settings中的“REST_FRAMEWORK”配置匿名用户对应的返回值时，request.user会返回对应的设置的值。
    5、其他认证类：BasicAuthentication,浏览器将用户名和密码加密，加密处理之后放在请求头中发送到页面中，以“弹出框”的形式去认证对应的用户用和密码

    注意：（文件导入问题解决）
    对应认证文件要和view层分离，直接将路径导入settings中的REST_FRAMEWORK即可，“注意如果发生模块找不到错误，利用sys方法”，之后
    若出现INSTALLED_APPS找不到app错误，要在对应的app名称前加上前缀。   认证文件路径：dj_study.view_CBV.rest_auth.auth
    
权限：
    1、和认证相似，与view分离，在其他文件中写对应希望实现的权限类
    2、“has_permission”源码自带权限方法，优先执行
    3、可以在settings中配置全局"DEFAULT_PERMISSION_CLASSES"或者直接导入使用。想执行非全局权限类的话，利用permission_classes = []去执行对应的权限类方法。若需要多个权限分类，就定义多个权限类方法即可。
    4、规范性规定：自定义的权限类必须继承“BasePermission”
    
节流（控制访问频率）
    1、和认证相似，与view分离，在其他文件中写对应希望实现的节流类
    2、“allow_request”源码自带权限方法，优先执行 
    3、可以在settings中配置全局"DEFAULT_THROTTLE_CLASSES"或者直接导入使用。想执行非全局权限类的话，throttle_classes = []去执行对应的节流类方法。若需要多个权限分类，就定义多个权限类方法即可。
    4、规范性规定：自定义的权限类必须继承“BaseThrottle”
版本
    
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
    permission_classes = []
    throttle_classes = [UserThrottle]
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
# 订单相关业务
# （只有SVIP用户有权限访问 --> 利用权限类方法）
class OrderView(APIView):

    # from dj_study.view_CBV.rest_auth.auth import Authentication      # 可以导入认证类直接使用或全局设置
    # authentication_classes = []                 # 执行认证类，为空则不认证

    # from dj_study.view_CBV.rest_auth.permission import MyPermission  # 可以导入权限类直接使用或全局设置
    # permission_classes = []                     # 执行权限类，为空则不需要权限

    # from dj_study.view_CBV.rest_auth.throttle import VisitThrottle     # 可以导入节流类直接使用或全局设置
    # throttle_classes = [VisitThrottle]           # 执行节流类，为空则不需要权限

    def get(self,request,*args,**kwargs):
        # self.dispatch
        ret = {'code': 1000, 'msg': None}
        try:
            ret["data"] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)

###############################################################

"""
1、版本(*)
2、解析器(*)
3、序列化(***)
    1.请求数据进行校验（django-form也可以校验）
    2.QuerySet进行序列化
4、分页(**)
5、路由(**)
6、视图(**)
7、渲染器(*)
"""

