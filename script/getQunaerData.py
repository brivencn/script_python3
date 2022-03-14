#!/usr/bin/env python

# -*- encoding: utf-8 -*-
"""
去哪儿网数据抓取

"""
import sys
sys.path.append("..")
import common.connectMysql as connmysql
import common.download as download
import time, requests, re, random, timeit
from lxml import etree  # 解析xpath网页结构


def getPage(url):  # 获取链接中的网页内容
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
        return page
    except Exception as e:
        # print(str(e))
        time.sleep(2)
        page = requests.get(url, headers=headers)  # 这里是请求网页数据了
        return page

def getList(address):
    place = address
    url = 'http://piao.qunar.com' + place
    timec = 20
    returnData = {
        'name': '',
        'open_info': '',
        'introduction_info': '',
        'img': []
    }
    while timec > 0:
        page = getPage(url)                 # 这里调用了getPage函数获取了网页数据
        # charset = page.apparent_encoding  # 网页 字符集
        selector = etree.HTML(page.text)    # 页面lxml.etree对象
        iscontinue = selector.xpath('.//div[@mp-role="pageContainer"]/div')
        # 获取图片地址 和 概述 以及 开放时间
        if len(iscontinue):
            view_name =selector.xpath('.//span[@class="mp-description-name"]/text()')[0]
            returnData['name'] = view_name
            print(view_name, '爬取中')

            introduction_info = iter(selector.xpath('.//div[@class="mp-charact-intro"]/div[@class="mp-charact-desc"]/p/text()'))
            # 获取描述文本
            while True:
                try:
                    returnData['introduction_info'] += '<p>' + next(introduction_info) + '</p>'
                except StopIteration:
                    break
            returnData['introduction_info'] = re.sub(r"'", '', returnData['introduction_info'])

            open_info = iter(selector.xpath('.//div[@class="mp-charact-time"]//div[@class="mp-charact-desc"]/p/text()'))
            # 获取开放时间文本
            while True:
                try:
                    returnData['open_info'] += '<p>' + next(open_info).replace('\r\n', '').strip() + '</p>'
                except StopIteration:
                    break
            returnData['open_info'] = re.sub(r"'", '', returnData['open_info'])

            img = iter(selector.xpath('.//div[@id="mp-slider-content"]/div[@class="mp-description-image"]/img/@src'))
            # 获取图片
            while True:
                try:
                     returnData['img'].append(next(img))
                except StopIteration:
                    break
            time.sleep(random.uniform(2, 3))
            break
        else:
            time.sleep(3)
            timec = timec - 1

    return returnData

def main():
    # 查出所有 景点
    with connmysql.UseMysql() as um:
        sql = "SELECT `id`,`detail_uri`,`version` FROM `view_list` WHERE id >= 1"
        um.cursor.execute(sql)
        data = um.cursor.fetchall()

    for i in range(0, len(data)):
        id = data[i]['id']
        now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 去哪儿网详情页
        detail_url = data[i]['detail_uri']
        # 获取爬虫数据
        ret = getList(detail_url)
        index = 0
        # 下载所有图片
        for img_one in ret['img']:
            if img_one == 'http://mp-piao-admincp.qunarzz.com/mp_piao_admin_mp_piao_admin/admin/20217/30d54820c6727b9958d585769ab3c5c2.png_710x360_c2302e12.png':
                continue
            if img_one == 'https://mp-piao-admincp.qunarzz.com/mp_piao_admin_mp_piao_admin/admin/20217/30d54820c6727b9958d585769ab3c5c2.png_710x360_c2302e12.png':
                continue
            img_one = re.sub(r'_710x360+.*', '', img_one)
            index += 1
            name = ret['name'] + '_' + str(index) + '.jpg'
            name = re.sub(r'[\\/:*?"<>|]', '_', name)
            down_ret = download.download_img(img_one, name)
            if down_ret > 0:
                try:
                    with connmysql.UseMysql() as um:
                        sql = "INSERT INTO view_img (`view_id`, `img`, `addtime`, `origin_name`, `origin_url`) VALUES ({}, '{}', '{}', '{}', '{}')".format(
                            id, name, now_date, '去哪儿网境内门票', img_one
                        )
                        um.cursor.execute(sql)
                except Exception as e:
                    print("-----------error to update -----------------")

            time.sleep(1)

        # 更新数据库
        try:
            with connmysql.UseMysql() as um:
                version = data[i]['version'] + 1
                sql = "update view_list SET `version` = {}, `updtime` = '{}', `open_info` = '{}', `introduction_info` = '{}'  where `id` = {}".format(
                    version, now_date, ret['open_info'], ret['introduction_info'], id)
                um.cursor.execute(sql)
        except Exception as e:
            print("-----------error to update -----------------")
        print(str(i) + '_已完成')
        time.sleep(1)

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    diff = timeit.default_timer() - start
    print("总共耗时: %.6f秒" % diff)
    exit(200)