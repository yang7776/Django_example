# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/10/23 17:33
# file_name     mongodb.py

from pymongo import MongoClient

'''
> : $gt
< : $lt
>= : $gte
<= : $lte
$in:(m,n,) : 提取在指定内容中的数据
$all[n,m,...]: 查找数据库中某一条数据是否全部包含all中的数据, 如果'全部'包含则返回该条数据,否则不反悔
$push: 向已有数据源中按照字段进行数据的添加.基于'列表'
$pop: 将数据库中对应数据的某一个字段数据按照指定方式进行删除. 其中 -1:从列表的起始位置开始删除; 1: 从列表的最后位置开始删除
$pull: 将对应数据中指定的数据分布进行删除(按值删除)
$or : 或者指令, 该指令通常作为字典的键, 其对应的值是一个'列表'结构,列表中每一个元素之间是'并列'的关系.
"在字典中所有的键值对之间代表的是一种'并且'的关系."
.sort('age',1): 将查找之后的结果按照指定的字段进行排序, 1为升序,-1为降序
.skip(m).limit(n): 将查找结果的取值显示为,跳过m条数据,显示n条数据.  即只显示m+1~m+1+n的数据
'''


class MongoData(object):

    def __init__(self, host, port, database, table):
        self.client = MongoClient(host=host, port=port)  # 若需要账号、密码，在括号中加入即可
        self.db = self.client[database]
        self.col = self.db[table]

    def insert(self, data):
        """添加数据"""
        if isinstance(data, dict):  # 插入一条数据
            ret = self.col.save(data)
            return ret

        elif isinstance(data, list):  # 插入多条数据
            error_data = []
            for i in data:
                if not isinstance(i, dict):
                    error_data.append(i)
                    data.remove(i)
                    continue
            ret = self.col.insert_many(data)
            if len(error_data) > 0:
                return "数据格式中检测有错误类型：%s" % error_data
            return ret

        else:
            return "数据格式为dict或者[{},{}]形式的列表但你传入的是：%s" % type(data)

    def find(self, data, flag=True):
        """查找数据"""
        try:
            if flag:
                res = self.col.find(data)  # 查多条数据
                result = []
                for i in res:
                    result.append(i)
                return result
            else:
                res = self.col.find_one(data)  # 查一条数
                return res
        except Exception:
            return "查询数据格式有误"

    def update(self, org_data, new_data, flag=True):  # flag = True  只更新一条
        """
        更新数据
        update:返回的是一个字典，字典中包括了操作更新结果和操作数据的个数
        update_one:只更新一条数据
        update_many：更新所有数据
        """
        if flag:
            ret = self.col.update_one(org_data, {"$set": new_data})  # 只更新一条
            return (ret, ret.modified_count)   # modified_count 返回更新的条数

        else:
            ret = self.col.update_many(org_data, {"$set": new_data})  # 更新全部数据
            return (ret, ret.modified_count)

    def field_update(self, action, org_data, new_data):
        """字段操作，注意action的操作仅针对于字段，且操作字段对应的数据类型必须是"array" !!!"""
        if action not in ["push", "pull", "pop"]:
            return "不支持的字段更新方式：%s" % action
        res = self.col.update(org_data, {"${}".format(action): new_data})
        return res

    def delete(self, data, flag=True):
        """删除数据"""
        if flag:
            ret = self.col.delete_one(data)  # 删除一条
            return ret
        else:
            ret = self.col.delete_many(data)  # 删除全部
            return ret

"""
if __name__ == "__main__":
    mongo = MongoData("localhost", 27017, "wallhaven", "recommend_img")
    data_insert = [
        {'name': 'jiesen', 'age': 13, 'sex': '男'},
        {'name': 'jiesen', 'age': 35, 'sex': '男'},
        {'name': 'jiesen', 'age': 23, 'sex': '男'}
    ]

    data_find = {'age': {'$gte': 5, "$lte": 35}}    # {'age':{'$in':(5,25)}
    data_update_or_delete = {"name": "jiesen"}

    # res = mongo.insert(data_insert)
    res = mongo.col.count()
    # res = mongo.update(data_update_or_delete,{"age":[1,2,3,4,5]})
    # res = mongo.delete(data_update_or_delete,flag=False)
    # res = mongo.field_update("pull", data_update_or_delete, {"age": {"name": "asdsasd"}})
    print(res)
"""