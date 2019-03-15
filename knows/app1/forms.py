# Django自带form组件
from django import forms

class UserInfo(forms.Form):
    # 定义form类，创建模型和前端form表单一一对应，required设定接收的是否可以为空
    username = forms.CharField(label="用户名",required=True,max_length=3,help_text="此项必填",
                               error_messages={'max_length':"最多三个字符"})
    iphone = forms.CharField(label="手机号",required=False)