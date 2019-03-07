# 提升python性能方法
# 博客地址：https://m.jb51.net/article/63166.htm


# 排序时，使用键值对方式，利用operate方法排序速度快，也支持多个关键字同时排序，同样适用与min(),max()等函数中的key关键字。
import operator

students = [
	{"name": "Stanley", "age": 22, "score": 92},
	{"name": "Peter", "age": 19, "score": 99},
	{"name": "Well", "age": 23, "score": 82},
	{"name": "Bob", "age": 20, "score": 88},
	{"name": "Lily", "age": 22, "score": 95}
]
students_by_score_age = sorted(students, key=operator.itemgetter("score", "age"), reverse=True)
print(students_by_score_age)
