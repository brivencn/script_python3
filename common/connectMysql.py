#!/usr/bin/env python

# -*- encoding: utf-8 -*-

"""
    mysql连接 连接池
    作者: 小肥巴巴
    简书: https://www.jianshu.com/u/db796a501972
    邮箱: imyunshi@163.com
    github: https://github.com/xiaofeipapa/python_example
    您可以任意转载, 恳请保留ta作为原作者, 谢谢.
"""

import pymysql
from timeit import default_timer
from dbutils.pooled_db import PooledDB

class PooleConfig:
    """

        :param mincached:连接池中空闲连接的初始数量
        :param maxcached:连接池中空闲连接的最大数量
        :param maxshared:共享连接的最大数量
        :param maxconnections:创建连接池的最大数量
        :param blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
        :param maxusage:单个连接的最大重复使用次数
        :param setsession:optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        :param reset:how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)

    """

    def __init__(self, host, db, user, password, port=3306):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password

        self.charset = 'UTF8'  # 不能是 utf-8
        self.minCached = 100
        self.maxCached = 100
        self.maxShared = 100
        self.maxConnection = 100

        self.blocking = True
        self.maxUsage = 100
        self.setSession = None
        self.reset = True

class DMysqlPoolConn:

    __pool = None

    def __init__(self, config):

        if not self.__pool:
            self.__class__.__pool = PooledDB(creator=pymysql,
                                             maxconnections=config.maxConnection,
                                             mincached=config.minCached,
                                             maxcached=config.maxCached,
                                             maxshared=config.maxShared,
                                             blocking=config.blocking,
                                             maxusage=config.maxUsage,
                                             setsession=config.setSession,
                                             charset=config.charset,
                                             host=config.host,
                                             port=config.port,
                                             database=config.db,
                                             user=config.user,
                                             password=config.password,
                                             )

    def get_conn(self):
        return self.__pool.connection()

def get_pool_conn(host, db, user, password, port):
    db_config = PooleConfig(host, db, user, password, port)
    return db_config

class UseMysql(object):

    def __init__(self, host='127.0.0.1', port=3306, db='51map', user='root', password='root'):
        self._host = host
        self._port = port
        self._db = db
        self._user = user
        self._password = password

    def __enter__(self):
        self._start_time = default_timer()

        # 从连接池获取连接
        db_config = get_pool_conn(self._host, self._db, self._user, self._password, self._port)
        g_pool_connection = DMysqlPoolConn(db_config)
        conn = g_pool_connection.get_conn()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()

        self._cursor.close()
        self._conn.close()

        # diff = default_timer() - self._start_time
        # print("程序耗时: %.6f秒" % diff)

    @property
    def cursor(self):
        return self._cursor

if __name__ == '__main__':
    with UseMysql() as um:
        um.cursor.execute("select count(id) as total from view_list where view_level = {}".format(5))
        data = um.cursor.fetchone()
        print("当前数据库中 AAAAA级别景区 有： {}个".format(data['total']))