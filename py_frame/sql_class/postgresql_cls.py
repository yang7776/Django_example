# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/8/1 12:05
# file_name     connect.py
import psycopg2
import os
import json

# 设置同级文件目录
path = os.path.join(os.getcwd(), 'postgresql_result.txt')


def write_res_to_file(path, result):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(result)
    else:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(result)


class PostgreConnect():
    def __init__(self, database, user, password, host, port=5432):
        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    # 执行命令
    def execute(self, sql_word):
        if not sql_word:
            raise Exception("sql word is format error!")
        self.cur.execute(sql_word)
        self.conn.commit()

    # 通过sql语句检索
    def select(self, sql_word):
        self.cur.execute(sql_word)
        rows = self.cur.fetchall()
        print(type(rows))
        print(rows)
        for row in rows:
            print(row)
        return json.dumps(rows)

    # 退出后关闭数据库
    def __del__(self):
        self.conn.close()
        self.cur.close()


if __name__ == '__main__':
    mc = PostgreConnect('cloudapi-engine', 'postgres', 'shining321', '182.92.102.90', 6190)
    result = mc.select('select * from wdad_vscontenttilegroup')
    write_res_to_file(path, result)
