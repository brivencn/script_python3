#!/usr/bin/env python

# -*- encoding: utf-8 -*-
"""
根据去哪儿网抓到景点的完整名称
抓取去哪儿网标签，但是这个标签不是很准，参考意义有限

"""

import common.connectMysql as connmysql # 数据库mysql连接池
import time, requests, re, random  # time用于延时，requests用于请求网页数据，json转换json数据格式，re正则 random 随机延时
from lxml import etree  # 解析xpath网页结构
import redis

def redisSetAdd(val):
    """
    Redis连接池
    :param val:
    :return: void
    """
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.sadd('tag', val)

def getPage(url):
    # 获取链接中的网页内容
    # 网络请求时需要包含较为完整的headers(请求头)
    # 这里的headers就是requests header的内容
    # 除了cookie 和 user-agent其他都和我的电脑一样
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'cookie': 'QN1=O5cv7V3FXX6RVSo2FsZGAg==; QN205=s%3Dgoogle; QN277=s%3Dgoogle; csrfToken=AUBSZ1SJgtl2cBX2HyuS2BTEXvmciXKc; _i=RBTKS082R8KxQVZx6JB9OtPmNyxx; QN269=1EDA0650022211EA926DFA163E72396C; fid=3ac01f31-9181-4ed7-a38a-5c0d137aefcc; QN99=1500; QN300=organic; QunarGlobal=10.86.213.148_-72515c99_16e4b45ba14_623b|1573223249997; _vi=hCXRv3fD46caoElZPDCXIreqcskT0Spj7f9XqyWhjfxmL_u3Y7xhSmU49JoeKnflmT0XtDD78wrAbOYIR_IG3FwU-fkUzn927J70W0JK0Iy219BfJnqA_WGLcMw_p8UHFhEtG9kQ-SOa3-aG4lJkhxTME8JhUdpjG4Kl7_X1KFGy; QN601=28e00ebdfc5eae6e44c48a34869c6dd1; QN163=0; QN667=B; QN48=09fd9580-c998-4f2a-bd31-516ddfaeb4f3; QN100=WyLlpKfov57mma%2Fngrl85aSn6L%2BeIl0%3D; QN243=19; JSESSIONID=568D43DF4624B99A32042DCC50F984B8; QN57=15732237429980.552477010226762; Hm_lvt_15577700f8ecddb1a927813c81166ade=1573223744; QN267=91363111d04a42d3; QN58=1573223742995%7C1573223864461%7C2; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1573223865; QN271=88a69a10-00a3-42e0-a9dd-dcd01d16ca04',
        'Host': 'piao.qunar.com',
        'Referer': 'http://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%'
                   'A8%E6%99%AF%E7%82%B9&region=&from=mpl_search_suggest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        page = requests.get(url, headers=headers)  # 这里是请求网页数据了
        if page.status_code == 200:
            return page
        else:
            return False
    except Exception as e:
        print(str(e))
        time.sleep(5)
        page = requests.get(url, headers=headers)  # 这里是请求网页数据了
        return page

def getList(keyword):
    url = 'https://piao.qunar.com/ticket/list.htm?keyword=' + keyword + '&region=&from=mpl_search_suggest'
    tags = ''
    page = getPage(url)  # 这里调用了getPage函数获取了网页数据
    if page == False:
        return False
    selector = etree.HTML(page.text)    # 解析html
    iscontinue = selector.xpath('.//div[@class="sight-subject"]/dl[@class="sight-subject-list"]/dd')    # 找节点
    # 数据获取
    if len(iscontinue) > 1:
        print('start', '-' * 10, '正在爬取第', keyword, '-' * 10)
        for i in range(1, len(iscontinue)):  # 获取必要信息
            tag = selector.xpath('.//div[@class="sight-subject"]/dl[@class="sight-subject-list"]/dd/@data-value')[i]
            if tags == '':
                tags = tag
            else:
                tags = tags + ',' + tag
            redisSetAdd(tag)
        return tags
    else:
        return False

def main():
    # 查出所有 景点
    with connmysql.UseMysql() as um:
        sql = "SELECT `id`, `name`,`version` FROM `view_list` WHERE tag_info is NULL"
        um.cursor.execute(sql)
        data = um.cursor.fetchall()
        print(len(data))

    for i in data:
        time.sleep(random.uniform(3, 5))
        print(i)
        now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 获取爬虫数据
        ret = getList(i['name'])
        print(ret)
        print(now_date)
        if ret == False:
            print('false')
        else:
            # 更新数据库
            try:
                with connmysql.UseMysql() as um:
                    version = i['version'] + 1
                    sql = "update view_list SET `version` = {}, `updtime` = '{}', `tag_info` = '{}' where `id` = {}".format(
                        version, now_date, ret, i['id'])
                    um.cursor.execute(sql)
            except Exception as e:
                print("-----------error to update -----------------")
            time.sleep(1)

if __name__ == '__main__':  # 代码是从main函数开始的
    main()

