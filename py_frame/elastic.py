# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/8/1 18:23
# file_name     elastic.py
# version：7.3.0（注意：info()里面的“number”是版本号）
from elasticsearch import Elasticsearch
es = Elasticsearch("127.0.0.1:9200")
# print(es.info())  # 可查看elasticsearch相关信息，测试连接
"""
创建/删除索引，如果检测到已创建，就会返回“400”错误。
注意：在插入数据的时候，也可以实现创建索引
:param index : 存储索引
:param ignore: 检索不到时，返回对应错误状态码
"""
# es.indices.create(index='t_index',ignore=404)
# es.indices.delete(index='t_index',ignore=404)

"""
映射数据库
参考博客：https://blog.csdn.net/woshixiazaizhe/article/details/81297194
type：（注意：版本不同，对应的类型也会有所改变）
字符串类型：string
日期类新：date
长整型：long
浮点型：float
双精度浮点：double
布尔类型：boolean
注意：如果一个字段需要被全文搜索的，应该设置为text类型；设置text类型之后，字段内容会被分析，
在生成倒排索引之前，字符串会被分词器分成一个一个词项；text类型的字段不用于排序

类型为 keyword 的字段只能通过精确值搜索到；keyword 类型适用于索引结构化的字段，比如主机名、
状态码等；通常用户过滤、排序、聚合。
在7.x版本中，string类型为text和keyword的结合

注意：使用ik分词器，必须下载ik插件：
	1、cd到\elasticsearch-7.3.0\bin目录下
	2、执行“elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.3.0/elasticsearch-analysis-ik-7.3.0.zip”，然后重启elasticsearch即可使用
	
:param analyzer：分析指定字段值时，拆分方式
:param search_analyzer：查询指定字段值时，检索方式
	ik_max_word：细粒度拆分,按照最大拆分可能性去检索，如输入“张三丰” 将拆分为：
	 '“张三丰”',“'张'”,“'三'”,“'丰'”,“'张三'”,“'张丰'”,'三丰'”
	ik_smart：粗粒度拆分
"""
mapping = {
	"id":{'type':'long'},
	"name":{u'analyzer': u'ik_max_word', u'type': u'text',u"search_analyzer": u"ik_smart"},
	"age":{'type':'long'},
	"sex":{u"type": u"text"}
}
body = {
	"properties": mapping
}
# 注意7.x版本，需要include_type_name=True
res_map = es.indices.put_mapping(include_type_name=True,index="t_index",doc_type='default',body=body)
print(res_map)

"""
插入数据
注意：插入数据时如果检测到没有对应的索引值，会先创建再插入，并不会因为检测不到索引而插入失败
:param index : 存储索引
:param ignore: 检索不到时，返回对应错误状态码
:param doc_type: 存储类型，一般默认为“default”
:param id: 单条数据的id值，相当于主键
:param body: 单条的完整数据，字典类型
"""
data = {
	"id":1,
	"name":"张三",
	"age":17,
	"sex":"男"
}
data1 = {
	"id":11,
	"name":"李四",
	"age":27,
	"sex":"男"
}
# es.index(index='t_index',doc_type="default",id=data["id"],body=data)
# es.index(index='t_index1',doc_type="default",id=data1["id"],body=data1)

"""
查询数据
get:根据id查询
search：根据条件（字典的值）查询，一般使用这个进行索引查询。
:param search -> body: 见下字典
{ "from": 0,  # 检索位置从哪里开始
  "size": 10, # 返回几条数据
  "query":{"match_all":{}},  # 返回全部查询结果
  "query":{'match':{'name':'张三'}}  # 返回指定数据查询结果
  ...更多请参考el文件，以及
}
"""
# 以下为级联查询
# query = {
# 	'query': {
# 		'bool': {
# 			'should': [  # 需要满足的条件
# 				{'match': {'scene': '夜宵,产品展示,单品推荐'}},
# 				{'match': {'color_style': '青色'}},
# 				{'match': {'pay_word': '人均50-100，早期'}},
# 				{'match': {'category': '美食,烧烤'}},
# 				{'match': {'human': '靠近旅游景点'}},
# 			],
# 			"minimum_should_match": 3,  # 起码匹配3个信息以上
# 			"must": [  # 必须满足的条件
# 				{'match': {'v_or_h': 0}}
# 			]
# 		}
#
# 	},
# 	"from": 0,
# 	"size": 5,
# 	"sort": [{"_score": {'order': 'desc'}}]  # 按相关性降序排序
# }

# 以下为全文多字段查询
# match= {
# 	"query": "零食",
# 	"fields": ["name", "desc", "custom_label", "color_style", "scene", "pk_str", "category", 	"pay_word", "human"],
# 	"operator": "or",  # 如果多字段，需要指明“operator”字段，or：指字段中一个有即可，and：全部字段中都匹配才可以
# }
# query = {
# 	'query': {
# 		'bool': {
# 			"must": [  # 必须满足的条件
# 				{'multi_match': match}
# 			]
# 		}
#
# 	},
# 	"from": 0,
# 	"size": 5,
# 	"sort": [{"_score": {'order': 'desc'}}]  # 按相关性降序排序
# }


# res = es.get(index='t_index',doc_type='default',id=1)
# res1 = es.search(index='t_index',body={"query":{"match_all":{}}})
# for hit in res1['hits']['hits']:
#     print(hit["_source"])
#
# res = es.search(index="t_index", body={'query':{'match':{'name':'张三'}}}) #获取any=data的所有值
# print(res)

"""
更新数据update
注意：“ignore=404”是检测如果没有对应的索引，则返回404错误；
body：对应的修改参数必须是字典，且键必须为“doc”，即{"doc":"?"}，其中的？可以修改一个，
也可以同时修改多个，看传的值；若“？”中修改的值对应数据检索不到，更会自动再创建一个字段，
将对应的值添加到数据中。
"""
data_up = {
	"id":1,
	"name":"小七",
	"age":17,
	"sex":"男",
	"new_key":"test"
}
# 一次传一个大字典，检索到对应key，就更改，检索不到，就添加。
# res = es.update(index="t_index",doc_type="default",body={'doc':data_up},id=1,ignore=400)
# res = es.update(index="t_index",doc_type="default",body={'doc':{'name':"小小七"}},id=1,ignore=404)
# print(res)

"""
删除数据
"""
# es.delete(index="t_index",doc_type='default',id=1)
