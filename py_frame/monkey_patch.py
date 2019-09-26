# coding=utf-8

# 猴子补丁
"""
在运行时动态修改已有的代码，而不需要修改原始代码。但是此补丁带了便利的同时也有搞乱源代码优雅的风险。
"""


# 例1：如想讲代码中导入的json统一更换为ujson，测试是否速度比json更快，
# 但由于导入量大，更改起来成本较高，此时可用猴子补丁动态改变

# import json
# import ujson
#
# def monkey_patch_json():
# 	json.__name__ = 'ujson'
# 	json.dumps = ujson.dumps
# 	json.loads = ujson.loads
# monkey_patch_json()
# print(json.__name__)

# 此时只需要在文件入口加上 monkey_patch_json() 即可


# 例2

class test:
    def func(self, x, y):
        return x + y


print("这是正常的结果：%s" % test().func(2, 5))


def monkey(self, x, y):
    return x * y


test.func = monkey
print("这是通过猴子补丁动态改变的结果：%s" % test().func(2, 5))
