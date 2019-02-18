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