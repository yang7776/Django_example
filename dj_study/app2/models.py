from django.db import models

TYPE = (
    (1, u"老师"),
    (2, u"非老师"),
)

class Teacher(models.Model):
    card_id = models.IntegerField(primary_key=True)
    type = models.SmallIntegerField(default=1, choices=TYPE, db_index=True)
    name = models.CharField(max_length=30)

class Major(models.Model):
    major_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    t_id = models.ForeignKey(Teacher,on_delete=models.CASCADE,default="",related_name="t_m")

class Student(models.Model):
    stu_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    classroom = models.CharField(max_length=100)
    major_id = models.ManyToManyField(Major)
    
class Test_item_Manger(models.Manager):
    def judge_id(self,test_id):
        if int(test_id)>7:
            return "test_id大于7"
        else:
            return "test_id小于7"
    
class Test_item(models.Model):
    test_id = models.IntegerField(primary_key=True)
    test_name = models.CharField(max_length=30)
    test_time = models.DateTimeField("创建时间",auto_now_add=True,db_index=True)
    # DateTimeField：注意此字段不用添加，会自动添加当前时间。但是有两个条件
    # 条件1：前端读取时，要数据格式化，显示对应的格式，如：{{ item.test_time|date:"Y-m-d H:i:s" }}
    # 条件2：在settings文件中，修改时区为亚洲上海，需要修改两个字段：TIME_ZONE = 'Asia/Shanghai'  USE_TZ = False
    create_time = models.DateTimeField("最近修改时间",auto_now=True,db_index=True)
    objects = Test_item_Manger()    # 相当于对模型中创造一个“不存在”的字段，而这个字段可以调用，对应的是一个“方法”
    class Meta:         # 更多“Meta”的属性，可看博客：https://blog.csdn.net/weixin_40933787/article/details/79425581
        app_label = "app2"     # 指定这个模型是在哪个工程下，一般用于不在对应app下创建的模型，然后指定这个模型属于谁
        db_table = "test_of_item"   # 指定这个模型的表名
        ordering = ["test_id"]      # 指定这个模型的排序根据哪个字段
        
        