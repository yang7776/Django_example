from django.db import models

# Create your models here.
def user_directory_path(instance, filename):
    # 获取文件后缀，可在以下进行判断
    ext = filename.split('.')[-1]
    # instance.selfid：代表下面模型中的数据，instance代表每一个实例
    return "{0}/{1}.{2}".format(instance.selfid, instance.name,ext)


class Person(models.Model):
    selfid = models.CharField(max_length=77,primary_key=True)
    name = models.CharField(max_length=77)
    photo = models.ImageField(blank=True,upload_to=user_directory_path)
    
class SeaTest(models.Model):
    id = models.IntegerField(primary_key=True)
    sex = models.CharField(max_length=30)
    age = models.IntegerField()
    name = models.CharField(max_length=50)
    
class User_Iphone(models.Model):
    username = models.CharField(max_length=5)
    iphone = models.CharField(max_length=20)