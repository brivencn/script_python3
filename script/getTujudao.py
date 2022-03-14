#!/usr/bin/env python

# -*- encoding: utf-8 -*-
"""
获取途居岛自驾营地信息
"""

import json
import time
import requests
import common.connectMysql as connmysql
import common.download as download

def getPage(url):
    headers = {
        'Host': 'api.v4.tujudao.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZTIxN2JlYzQ3YWQwNDQ1MjhlZTUyOWYxMDM2ZTcwMmE1OGQ3NWM1NDZhMDAwNDg5YTU0MjBiM2NjZjcxZWJhNjQ0MDIwYWRjZDE1NTRlMWMiLCJpYXQiOjE2Mzk1NjI3NDMsIm5iZiI6MTYzOTU2Mjc0MywiZXhwIjoxNjQyMTU0NzQzLCJzdWIiOiIiLCJzY29wZXMiOlsiKiJdfQ.hBUc-Foco01_lw5-h9ypvIDqa0fSxGhko1-UloUa1NJSMm15Wms0ZTNquuPtc919qbkcpVMXMrbqyACdYGYDk9Dhk-Es06Zs6a0OafzdMun_tG_ERrTVZsODV5YHaUeDbkTVGlQlO_NySfTKiSwefyTHRN3f7KnWjwRtcDBcIO9MrlHEJu3J2nRGv-Dtqr1rXwlGJxcoOsns0BEMOrHiDuw1Tur2nmh1UmDmHFcWgxOnWPV13_tqi6LGZ1D_hcXY_enUjUdwzAPzVCe2n1EoG3m06WY96o_fBbS7P4GLoAZsP8Jpdu5ceE7sMW8NcWRUozeApIlY7ySBzCFABPgdm38Sf8E4kCylwq365LJeCsX7U5F3Y0VG--ilECLXbUNLG5WMSt1kplr2u1LDI9udew-me2rZCk7vFte6n66dJT7Vw3v3wAhUBaDfssSAgqMiSmKrVuzMoJcP9qTqR23Z7ReSjrVejaE6e8YV3d9US46md0TF9UIkuDwKyV3Cr3qFrc3GjGddn-HIP9jyqaAwmNGeJSK-QwF9SuzgUTQGEW9gcT_nusGVKa5OToy7MQzYm7AqkjLywqVeM5yr38xlVIIRiTJOabLFOEsdfUd7S3B5nJrPtDLyg88zEql3C6Ai6YG-4lLFueoeTwRn8FcYmh5jdXK2TD76uSNb1dgiwI8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type': 'application/x-www-form-urlencoded',
        'Referer': 'https://servicewechat.com/wxec78c1176b7414da/119/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    try:
        page = requests.get(url=url, headers=headers, timeout=5)  # 这里是请求网页数据了
        return page
    except Exception as e:
        time.sleep(2)
        page = requests.get(url=url, headers=headers, timeout=8)  # 这里是请求网页数据了
        return page


def getJson():
    path = './file/camp.json'
    with open(path, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)

    for i in json_data['message']['data']:
        print(i)
        url = 'https://api.v4.tujudao.com/api/client/store?id={}&lat={}&lng={}&place=LIST169'.format(i['id'], i['lat'],
                                                                                                     i['lng'])
        print(url)
        ret = getPage(url)
        item_data = ret.json()
        # 写入数据库
        try:
            with connmysql.UseMysql() as um:
                now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if (i['is_pay'] == 1):
                    i['is_pay'] = '收费'
                if (i['is_pay'] == 0):
                    i['is_pay'] = '免费'
                print(json.dumps(item_data['message']['tags']))
                sql = "INSERT INTO camp_list (`name`, `province`, `heat`, `address`, `longitude_gaode`, " \
                      "`latitude_gaode`, `introduction`, `addtime`, `open`, " \
                      "`code_id`, `is_free`, `tags`, `name2`, `description`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                    item_data['message']['provider']['name'], '', '1', item_data['message']['address'], i['lng'],
                    i['lat'], item_data['message']['intro'], now_date,
                    '{}-{}'.format(item_data['message']['open_time'][0:5], item_data['message']['close_time'][0:5]),
                    i['id'], i['is_pay'], json.dumps(item_data['message']['tags'], ensure_ascii=False), i['name'], item_data['message']['desc']
                )
                um.cursor.execute(sql)
                sql = "SELECT  LAST_INSERT_ID() as id;"
                um.cursor.execute(sql)
                ids = um.cursor.fetchall()
                print(ids[0]['id'])
                # 下载所有图片
                for img_url in item_data['message']['files']['LIST169']:
                    split_img = img_url.split(".")
                    ext = split_img[len(split_img) - 1]
                    name = split_img[len(split_img) - 2].split("/")
                    name = name[len(name) - 1]
                    name = "{}.{}".format(name, ext)
                    down_ret = download.download_img(img_url, name)
                    if down_ret > 0:
                        with connmysql.UseMysql() as um:
                            sql = "INSERT INTO camp_img (`camp_id`, `img`, `addtime`, `origin_name`, `origin_url`) VALUES ({}, '{}', '{}', '{}', '{}')".format(
                                ids[0]['id'], name, now_date, '途居岛自驾营地', img_url
                            )
                            um.cursor.execute(sql)

        except Exception as e:
            print("-----------error to update -----------------")

        print('this finished')
        time.sleep(5)
getJson()

