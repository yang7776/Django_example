# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/23 17:33
# file_name     redis.py

from gevent import socket as gevent_socket
import redis
import pickle

REDIS_HOST = "localhost"
REDIS_PORT = 6379
_conn_pool_db = None    # 设置redis连接池，当连接成功，则不再为None，防止二次连接

# REDIS_PASSWORD = ''

class RedisDB():
	# tae master db
	def __init__(self, dbIdx=0):
		self.host = REDIS_HOST
		self.port = REDIS_PORT
		self.db = dbIdx
		# self.password = REDIS_PASSWORD
		self.patch_green = 0   # 设置一个参数判断gevent是否启动
	
	def conn(self):
		if True:   # 可以设置一个条件来决定，是否将redis设置为非阻塞
			redis.connection.socket = gevent_socket   # 将redis连接设置为异步非阻塞化连接，即解决了io阻塞的问题（猴子补丁思想）
			self.patch_green = 1
		
		global _conn_pool_db
		if not _conn_pool_db:
			_conn_pool_db = redis.ConnectionPool(
				host=self.host,
				port=self.port,
				db=self.db,
				# password=self.password,   # 有密码就加上
				socket_timeout=5  # 连接超时
			)
		self.redis = redis.StrictRedis(connection_pool=_conn_pool_db)
	
	def add_value(self, key, value, type="", expire_tm=None):
		"""
		:param key: key
		:param value: value
		:param type: 默认为空，可为同类型的key，value加上type参数，方便维护，增加可读性。在数据库可视化界面中，同类型是在同一个文件夹下。
		:return: Redis Setnx（SET if Not eXists） 命令在指定的 key 不存在时，为 key 设置指定的值
		"""
		self.conn()
		redis = self.redis
		value = self.__set_value(value)
		key = self.__get_name(key, type)
		redis.setnx(key, value)
		if isinstance(expire_tm, int):
			self.redis.expire(key,expire_tm)
	
	def add_values(self, value, type="", expire_tm=None):
		"""
		:param value: {"key1":"value1" , "key2":"value2" , ...}
		:param type: 默认为空，可为同类型的key，value加上type参数，方便维护，增加可读性。在数据库可视化界面中，同类型是在同一个文件夹下。
		:return:
		"""
		self.conn()
		if not isinstance(value, dict):
			return
		for key, val in value.items():
			_value = self.__set_value(val)
			key = self.__get_name(key, type)
			self.redis.set(key, _value)
			if isinstance(expire_tm, int):
				self.redis.expire(key, expire_tm)
	
	def delete_value(self, key, type=""):
		self.conn()
		key = self.__get_name(key, type)
		self.redis.delete(key)
	
	def reset_value(self, key, value, type="", expire_tm=None):
		self.conn()
		redis = self.redis
		value = self.__set_value(value)
		key = self.__get_name(key, type)
		redis.set(key, value)
		if isinstance(expire_tm, int):
			redis.expire(key, expire_tm)
	
	def get_value(self, key, type=""):
		self.conn()
		key = self.__get_name(key, type)
		key_type = self.redis.type(key)
		if key_type == b'string':   # 字符串
			value = self.redis.get(key)
		elif key_type == b'set':    # 集合
			value = self.redis.smembers(key)
		elif key_type == b'hash':   # 哈希
			value = self.redis.hgetall(key)
		elif key_type == b'list':   # 列表
			value = self.redis.lrange(key, 0, -1)
		elif key_type == b'zset':   # 有序级
			value = self.redis.zrange(key, 0, -1)
		else:
			value = None
		if value is None:
			return value
		return pickle.loads(value)
	
	def __set_value(self, value):
		"""将value转化加密"""
		return pickle.dumps(value)
	
	def __get_name(self, key, type):
		if type:
			return "%s:%s" % (type, key)
		else:
			return key
	
	def flushdb(self):
		# Flushdb 命令用于清空当前数据库中的所有 key。
		self.conn()
		self.redis.flushdb()
	
	def close(self):
		#        self.redis.close()
		pass


if __name__ == "__main__":
	redis_oper = RedisDB()

	# redis_oper.add_value("test_key", "test_value")
	# res = redis_oper.get_value("test_key")
	
	# redis_oper.add_values({"type":"v1","type2":"v2"},"11",600)
	# res = redis_oper.get_value("type1","11")
	
	# redis_oper.reset_value("test_key","test_value777")
	# res = redis_oper.get_value("test_key")
	
	# redis_oper.delete_value("test_key")
	
	# redis_oper.flushdb()
	
	# print(res)