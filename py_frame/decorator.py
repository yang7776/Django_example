# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/7/8 15:32
# file_name     decorator.py

# 不带参装饰器
def y_a(fun_a):
	def wrap():
		print(fun_a.__name__)
		return fun_a()
	return wrap
@y_a
def a():
	print("aaa")
	
# 带参数装饰器（其实就是无参装饰器外面在套一层）
def y_b(s):
	
	def wrap(fun):
		def f():
			print(s)
			return fun()
		return f
		
	return wrap
	
@y_b('this is a param')
def b():
	print("aaa")
	
a()
print('==========================================')
b()

	

