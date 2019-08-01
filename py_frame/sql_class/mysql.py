# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/8/1 14:30
# file_name     mysql.py
import pymysql


class MysqlConnect(object):
	# 魔术方法, 初始化, 构造函数
	def __init__(self, host, user, password, database):
		'''
		:param host: IP
		:param user: 用户名
		:param password: 密码
		:param port: 端口号
		:param database: 数据库名
		:param charset: 编码格式
		'''
		self.db = pymysql.connect(host=host, user=user, password=password, port=3306, database=database, charset='utf8')
		self.cursor = self.db.cursor()
	
	# 执行命令
	def execute(self, sql):
		# 执行SQL语句
		self.cursor.execute(sql)
		# 提交到数据库执行
		self.db.commit()
	
	# 通过sql语句检索
	def select(self, sql):
		self.cursor.execute(sql)
		# 获取所有记录列表
		results = self.cursor.fetchall()
		for row in results:
			print(row)
	
	# 退出后关闭数据库
	def __del__(self):
		self.cursor.close()
		self.db.close()


if __name__ == '__main__':
	mc = MysqlConnect('127.0.0.1', 'root', 'ysh7776...', 'y_test')
	# mc.execute(
	# 	"CREATE TABLE person (`id` int(11) NOT NULL,`sex` varchar(30) NOT NULL,`age` int(11) NOT NULL,`name` varchar(50) NOT NULL,PRIMARY KEY (`id`))"
	# )
	# mc.execute(
	# 	"insert into person(id, sex, age, name) value (1,'男',17,'张三')"
	# )
	mc.select('select * from person')
