# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/10/15 15:27
# file_name     epoll_03.py

# todo gevent通过socket补丁实现redis.py非阻塞

import gevent
import redis
import redis.connection

redis.connection.socket = gevent.socket
r = redis.StrictRedis()
p = r.connection_pool

# redis实例封装
class RedisDB():
    #tae master db
    def __init__(self, dbIdx=0):
        self.host = redis_config.REDIS_HOST
        self.port = redis_config.REDIS_PORT
        self.db = dbIdx
        self.password = redis_config.REDIS_PASSWORD
        self.patch_green = 0

    def conn(self):
        if int(os.environ.get("IS_GEVENT","0")) > 0 :
            redis.connection.socket = gevent.socket
            self.patch_green = 1

        global _conn_pool_db
        if not _conn_pool_db :
            _conn_pool_db = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password, socket_timeout=5)
        self.redis = redis.StrictRedis(connection_pool=_conn_pool_db)

    def flushdb(self):
        self.conn()
        self.redis.flushdb()

    def __set_value(self,value):
        return pickle.dumps(value)

    def add_value(self,name,value,type=""):
        self.conn ()
        redis = self.redis
        value = self.__set_value(value)
        key = self.__get_name(name,type)
        redis.setnx(key,value)

    def reset_value(self,name,value,type="", expire_tm=None):
        self.conn ()
        redis = self.redis
        value = self.__set_value(value)
        key = self.__get_name(name,type)
        redis.set(key,value)
        if isinstance(expire_tm, (int, long)):
            redis.expire(key, expire_tm)

    def add_values(self, value, type=""):
        self.conn ()
        if not isinstance(value,dict):
            return
        # pipe = self.redis.pipeline()
        for key, val in value.iteritems():
            _value = self.__set_value(val)
            key = self.__get_name(key,type)
            self.redis.set(key,_value)
            # if key_type == "string":
            #     pipe.set(key, _value)
            # else:
            #     pipe.rpush(key, _value)

        # pipe.execute()

    def get_value(self, name, type="", host="slave"):
        """
        :param name:
        :param type:
        :param host:  "master" , "slave"
        :return:
        """

        if not getattr(redis_config, "SLAVE_REDIS_ACTIVE", False) or not getattr(redis_config, "SLAVE_REDIS_NODES"):
            host = None
        if host == "slave":
            return SlaveRedisDB(dbIdx = self.db).get_value(name,type=type)
        else:
            self.conn()
            key = self.__get_name(name,type)
            key_type = self.redis.type(key)
            if key_type == 'string':
                value = self.redis.get(key)
            elif key_type == 'hash':
                value = self.redis.hgetall(key)
            elif key_type == 'zset':
                value = self.redis.zrange(key, 0, -1)
            else:
                value = None
            if value is None:
                return value
            return pickle.loads(value)

    def __get_name(self,name,type):
        if type:
            return "%s:%s" % (type,name)
        else:
            return name

    def close(self):
#        self.redis.close()
        pass