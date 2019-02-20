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
        if test_id>7:
            return self.get(test_id=test_id).test_name
        else:
            return "test_id小于7"
    
class Test_item(models.Model):
    test_id = models.IntegerField(primary_key=True)
    test_name = models.CharField(max_length=30)
    test_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now=True,db_index=True)
    objects = Test_item_Manger()    # 相当于对模型中创造一个字段，但是这个字段对应的是一个“方法”
    class Meta:         # 更多“Meta”的属性，可看博客：https://blog.csdn.net/weixin_40933787/article/details/79425581
        app_label = "app2"     # 指定这个模型是在哪个工程下，一般用于不在对应app下创建的模型，然后指定这个模型属于谁
        db_table = "test_of_item"   # 指定这个模型的表名
        ordering = ["test_id"]      # 指定这个模型的排序根据哪个字段
        
        