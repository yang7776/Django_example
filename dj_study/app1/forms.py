# Django自带form组件
from django import forms

iphone_regex = r"^((\+86)?|\(\+86\))0?1[3456789]\d{9}$"

class UserInfo(forms.Form):
    # 定义form类，创建模型和前端form表单一一对应，required设定接收的是否可以为空
    username = forms.CharField(label="用户名",required=True,max_length=3,help_text="此项必填",
                               error_messages={'max_length':"最多三个字符"})
    iphone = forms.RegexField(required=True, max_length=11, min_length=11, help_text=u"请正确填写手机号码！",regex=iphone_regex, error_messages={
            "required": u"此项必填！",
            "max_length": u'请输入不超过11字符！',
            "min_length": u'请输入起码11字符！',
            'invalid': u'请正确填写手机号码！'
        })



    # cinema_ip = forms.CharField(required=True, help_text=u"请正确填写影院IP", max_length=15, min_length=7, regex=ip_regex,
    #                             error_messages={
    #                                 "required": u"此项必填", "max_length": u'请输入不超过{0}字符'.format(15),
    #                                 "min_length": u'请输入不超过{0}字符'.format(7), 'invalid': u'请正确填写影院IP'
    #                             })
    # repair_per_tel = forms.RegexField(required=True, max_length=11, min_length=11, help_text=u"请正确填写手机号码",
    #                                   regex=iphone_regex, error_messages={
    #         "required": u"此项必填", "max_length": u'请输入不超过11字符', "min_length": u'请输入不超过11字符', 'invalid': u'请正确填写手机号码'
    #     })
