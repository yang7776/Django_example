# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/8/1 12:05
# file_name     connect.py
import psycopg2
class PostgreConnect():
	def __init__(self,database,user,password,host,port=5432):
		self.conn = psycopg2.connect(database=database,user=user,password=password,host=host,port=port)
		self.cur = self.conn.cursor()

	# 执行命令
	def execute(self,sql_word):
		if not sql_word:
			raise Exception("sql word is format error!")
		self.cur.execute(sql_word)
		self.conn.commit()
		
	# 通过sql语句检索
	def select(self,sql_word):
		self.cur.execute(sql_word)
		rows = self.cur.fetchall()
		for row in rows:
			print(row)
		
	# 退出后关闭数据库
	def __del__(self):
		self.conn.close()
		self.cur.close()
		
if __name__ == '__main__':
	mc = PostgreConnect('cloudapi-engine', 'postgres', 'shining321', '182.92.102.90',6190)
	mc.select('select * from wdad_vscontenttilegroup')
