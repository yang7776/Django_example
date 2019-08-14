from django.db import models
user_type_choices = (
    (1,'普通用户'),
    (2,'vip'),
    (3,'SVIP'),
)

class UserInfo(models.Model):
    user_type = models.IntegerField()
    username = models.CharField(max_length=77,unique=True)
    password = models.CharField(max_length=77)

class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo',on_delete=None)
    token = models.CharField(max_length=77)
