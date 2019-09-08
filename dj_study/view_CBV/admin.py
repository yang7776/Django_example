from django.contrib import admin

from dj_study.view_CBV.models.rest_model1 import *
from dj_study.view_CBV.models.rest_model2 import *
# Register your models here.
# rest1
admin.site.register(UserInfo)
admin.site.register(UserToken)

# rest2
admin.site.register(UserTokenT)
admin.site.register(UserInfoT)
admin.site.register(Role)
admin.site.register(UserGroup)
