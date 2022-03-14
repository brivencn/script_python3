#!/usr/bin/env python

# -*- encoding: utf-8 -*-
"""
高德经纬度转换
"""
import sys
sys.path.append("")
import common.connectMysql as connmysql
import grequests
import time
import timeit
# from threading import Thread

# 错误个数
fail = 0
# 偏移量
offset = 0

# 错误handler
def err_handler(request, exception):
    global fail
    fail += 1
    print(request, exception, '粗错了')

# 并发请求
def api_send_concurrent(data, coordsys = 'baidu'):
    r = []
    for i in range(0, len(data)):
        r.append(grequests.get('https://restapi.amap.com/v3/assistant/coordinate/convert?key=bc1922eee943676bb85e68d283187965&locations={},{}&coordsys={}'.format(data[i]['longitude_baidu'], data[i]['latitude_baidu'], coordsys)))
    res_list = grequests.map(r, exception_handler=err_handler)
    return res_list

# 分页查数据100条
def get_sqldata(offset, limit):
    with connmysql.UseMysql() as um:
        um.cursor.execute("select id,longitude_baidu,latitude_baidu from view_list limit {}, {}".format(offset, limit))
        data = um.cursor.fetchall()
        return data

# 更新数据
def upd_sqldata(ret, now_date, id):
    with connmysql.UseMysql() as um:
        longlat = ret['locations'].split(",", 1)
        sql = "update view_list SET `version` = 1, `addtime` = '2021-10-21 00:00:00', `updtime` = '{}', `longitude_gaode` = '{}', `latitude_gaode` = '{}'  where `id` = {}".format(now_date, longlat[0], longlat[1], id)
        um.cursor.execute(sql)

# 多线程处理
def do_thread(data, res_list):
    for i in range(0, len(res_list)):
        now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        upd_sqldata(res_list[i].json(), now_date, data[i]['id'])

def main():
    global offset
    limit = 100
    while True:
        # 查数据从0偏移，一次100条
        data = get_sqldata(offset, 100)
        # 查数据为空时 停止循环，结束
        if len(data) == 0:
            break
        # 下一次的偏移量
        offset += limit
        res_list = api_send_concurrent(data, 'baidu')
        do_thread(data, res_list)


if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    diff = timeit.default_timer() - start
    print("总共耗时: %.6f秒" % diff)
    print(fail)