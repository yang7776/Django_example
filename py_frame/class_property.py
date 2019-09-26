# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/7/8 15:30
# file_name     y_class.py


class Person:
    def __init__(self, name, age):
        self.name = name  # 公有变量：可以直接用“print(a.name)”输出，并修改
        self.__age = age  # 私有变量：外界不能访问，不能用“print(a.__age)”直接输出，但是可以通过“print(a._Person__age)”输出（多用于调试）

    def y_name(self):
        print(self.name)

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if 0 < age <= 120 and isinstance(age, int):
            self.__age = age
        else:
            raise ValueError('数字必须在1~120之间')


A = Person('liming', 17)
print(A.age)
A.y_name()
A.age = 77  # 通过@property方法，可将setter中的属性，如一些判断功能，直接赋予对应的函数中，相当于给一个方法中多加了一个功能
print(A.age)

# 输出结果
# 17
# liming
# 77
