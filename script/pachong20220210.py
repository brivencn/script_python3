#!/usr/bin/env python

# -*- encoding: utf-8 -*-
"""
去哪儿网数据抓取
1.入园公告 小贴士
2.用户评价

"""
import common.connectMysql as connmysql
import time, requests, re, random, timeit, json
from lxml import etree  # 解析xpath网页结构


def getPage(url):  # 获取链接中的网页内容
    # 网络请求时需要包含较为完整的headers(请求头)
    # 这里的headers就是requests header的内容
    # 除了cookie 和 user-agent其他都和我的电脑一样
    headers = {
        'Accept': 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'Connection': 'keep-alive',
        'cookie': 'SECKEY_ABVK=vK3qodbdxhISdk1LV0TpbYVkhiS9nMERU+DufBh9m/I%3D; BMAP_SECKEY=matWal5NcEmdTuhgWcWz9cGIqvQj2tK1tJoRYVOicDEg-x1-vF_w-StEslLTQj-EklXfexzoYEYuSBiRs6Mh195aRGLwHO7TDftJ28WWOtiE6_keCNQz3W1ONbjpltR-iZh8A8fL5pmbfxm2xzTr-nVks-m8rXIcgbAW3KvxIB4dgxrfgE5GQR4ngsKCjBmT; QN1=00008580306c3984fc90833e; QN300=auto_4e0d874a; QN99=9247; csrfToken=nGul3vUvbuPM9neM9wFQFEnoFW8eHscy; _i=DFiEuYMzleLwGIe6-CARQ2d_jCvw; QN601=886e0cc254142ead4e52a90bd4f6fb75; QunarGlobal=10.86.213.148_-332dc806_17cc4f2acd7_-3e2d|1635391891453; QN163=0; QN48=000088002f103984fc989e11; QN667=B; QN6=auto_4e0d874a; fid=366977bf-6407-4162-a46e-406225a946d0; QN57=16353918958250.5037622739708709; ctt_june=1635411815131##iK3wVR3mauPwawPwa%3DXsXs3nEDiGWKX%3DXS2%2BaKERWK2AERDAaS2naSXNWDawiK3siK3saKjsWSP%3DaRg%3DVKX%2BWUPwaUvt; ctf_june=1635411815131##iK3waKPsWwPwawPwa%3D3wasgmXSfRWR3%3DVKvmE2PmXsa8aSfhXP3sXStAEPDniK3siK3saKjsWSP%3DaRg%3DVKXmWhPwaUvt; cs_june=f6eb45fb177ffc7b1a1adcaf4660700a27ebe6b167c763b6d541a7a193a46e3ca19d69b5c3b258949bbfc43b9d280dbc32030e943c65fb38aea06818e9299e17b17c80df7eee7c02a9c1a6a5b97c1179bb6f427eedd7e1cbd8239f6fdf39c9035a737ae180251ef5be23400b098dd8ca; QN66=auto_4e0d874a; QN69=auto_4e0d874a; QN1231=0; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; QN25=d2307eb2-c6ac-447b-b59c-dba9d7818253-9f992f90; Hm_lvt_15577700f8ecddb1a927813c81166ade=1643020797; QN71="MTI1Ljg0LjgxLjIyMjrph43luoY6MQ=="; QN277=organic; QN205=organic; QN269=24E674508A1211ECA464FA163EB096A9; QN83=qunar; Hm_lvt_872c8902458e482752d6b30a0135dcd0=1644463048; Hm_lpvt_872c8902458e482752d6b30a0135dcd0=1644463330; QN63=%E4%B8%8A%E6%B5%B7%E9%87%8E%E7%94%9F%E5%8A%A8%E7%89%A9%E5%9B%AD%7C%E9%87%8D%E5%BA%86%7C%E5%9C%9F%E6%8B%A8%E9%BC%A0%E4%BF%B1%E4%B9%90%E9%83%A8%C2%B7%E5%84%BF%E7%AB%A5%E6%B2%89%E6%B5%B8%E5%BC%8F%E5%AE%9D%E8%97%8F%E4%B9%90%E5%9B%AD%7C%E9%BB%84%E6%B5%A6%E6%B1%9F%E6%B8%B8%E8%A7%88%7C%E9%BB%84%E6%B5%A6%E6%B1%9F%E6%B8%B8%E8%A7%88%EF%BC%88%E5%8D%81%E5%85%AD%E9%93%BA%E7%A0%81%E5%A4%B4%EF%BC%89%7C%E9%BB%84%E6%B5%A6%E6%B1%9F%E6%B8%B8%E8%A7%88(%E5%8D%81%E5%85%AD%E9%93%BA%E7%A0%81%E5%A4%B4)%7C%E4%B8%8A%E6%B5%B7%E6%B5%B7%E6%98%8C%E6%B5%B7%E6%B4%8B%E5%85%AC%E5%9B%AD%7C%E6%83%85%E4%BA%BA%E6%A0%91%7C%E9%A6%99%E6%A0%BC%E9%87%8C%E6%8B%89%E5%A4%A7%E5%B3%A1%E8%B0%B7%E5%B7%B4%E6%8B%89%E6%A0%BC%E5%AE%97%7C%E5%A4%A7%E4%B8%B0%E4%B8%8A%E6%B5%B7%E7%9F%A5%E9%9D%92%E7%BA%AA%E5%BF%B5%E9%A6%86%7C%E5%8C%97%E4%BA%AC%7C%E4%B8%8A%E6%B5%B7%E8%BF%AA%E5%A3%AB%E5%B0%BC%7C%E4%B8%9C%E6%A1%A5%E9%92%9F%E9%BC%93%E5%AF%A8%7C%E6%AD%A6%E5%AE%81%E9%B2%81%E6%BA%AA%E6%B4%9E; QN67=15477%2C37523%2C41794%2C198096%2C198098%2C14770%2C469608%2C456725%2C37365%2C7698; QN267=1132110594f1153411; _vi=i-S4dvBPsgUFICuXv15_IgNvCI9UraSO4lFPwl3i7zRonApO-pRcA52DyfqMEZg1z1Yqy2R8B5uUvajVK88q5Dv1L3K8ubZUnJuKMpO5auHJdR1G3pj0gs3bCskdgLQo7ppwoFGlfzf4p0_kiqGUgrvCXqFPTG7aPn6z-eS3m1Xp; ariaDefaultTheme=undefined; QN58=1644474776267%7C1644479001908%7C26; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1644479002; QN271=479846de-ccfd-44f5-8826-4ea506ec43ae; JSESSIONID=CBFFB9121AA83964B2522D10315371DE; __qt=v1%7CVTJGc2RHVmtYMStwMTNua3A3NWRVQm1ja0NBN0xXRTIwd0hPRmtlZ0NOT3o5T1dyS2YwaUc0VVFTc3lTam52bU9wVTZJNU1sZkx6QnZ3eDlMektpVWxqV0dPQkJaTmNMNlhHNDN1T1YyS2FUZkd2YWxIRk90cGhxaE1HM3RVZ0NZZ2F0T0I1dGJEbUVuSERzUngzdHhjV1F1SmtmM0dITTlhaG04WFgzQXJNPQ%3D%3D%7C1644479029823%7CVTJGc2RHVmtYMTlNd2RBNXJxejg3b1VFMXMvT3p6a0ZGV2VxSldvdzkvNUJkSjVDeXBnNWZSZ29aVU81aVh5OG5DNUJRaWNkYVRMWHF1cVF1b21nc1E9PQ%3D%3D%7CVTJGc2RHVmtYMTlkK25waHVVMVpqNXVmMDYrK0orcytwS1RJdGJ4aVp5cGFiT2xHMDhWazI3cFk1aHFtSHNMcHhhaFdFWVRNV0xkQkUxVmlDRk0zVlBPRHcvMzVaeE1lcHpGM1VRYjJtT25ZbE0xOHVqV0d2QUtDMUFwMzBQZmxkUGpaZ1NYY2xRVk1NMy9GbGhkM2lTSkUrRStrbDFYNUFhdFI3emVwTEFKRE43dUpRbGcxeHFKV0RGZUhXamJXVTNHbzZPQlRxcDI5UHRpVDRjRlNhU3BHdXU1NnIwTEJ3WDEyVjJTekJzUzlYcUVJZVdrUlBCZ3pOaVBxMlBFODY5aDliRUI1UzRsM3BMcmdZK0V1ZUoxWGhLZ2JET2pjUGNqOW9wOW9xaldLaWV3R0k3cnoyb2ZFTnhMM04zWmp1ZWdFTVo1bXQvL1RXOWRNRnY4byt5OW9NSTZRY2VnQkF2d2NDUXo0aVJ5SG5EZG9NRCswdHRTZ1hXa3FuRzlFWTJ1aWRvbFhWRTh6TzByVjVoc05veUpPOTM5aWIzNTJ0amt0TEVnRlJwL0d2TTUwckpzV0hIb3ZTSHpIb2NnQ2I4cFkxY1lPeTFQM1RpSk0zYXQ2emo1RlN2OVR1TFhwclBtODJaUHYxK3Nsc0VZVWZ5Q2RWV1FZeGNhZERWTmFGMEZDQ2pyTGh5RFRkZmtEVi9JRmpjS0tRR2x5NDNvR2FqOUNFTlhUZzM5L3JYUEhuUnNZTmg4cVFqek10cUdRZnVWbkc1cHo3c0hEZTVhYjFJZjlNWWpHR3F2c2NLQXh5bFJ1NHU3OU1yZXNDa2MwVFNmVDZOSWt2UkxURmZnakl6VGQwV3dYNU1DMWtrM1Y4SUd3REp0ZjB1WkVzZWI2N3QvYkw0MFA4WCs2dEFSclhxdXJ0WDJ5SlU0NFJWSjFlU0hIQ2p1dkppU1QvZDF5OUVyMzFKUkEySU1WR2NnbGFDMEhsNWYzRHg3cEwrYVMrOXBmOUxNNzQ1ZDZuQXcyMHc5WUsrOTM3QVpQTldyZjFPSWgwdz09',
        'Host': 'piao.qunar.com',
        'Referer': 'https://piao.qunar.com/ticket/list.htm?keyword=%E4%B8%8A%E6%B5%B7%E9%87%8E%E7%94%9F%E5%8A%A8%E7%89%A9%E5%9B%AD&region=&from=mpl_search_suggest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'
    }
    try:
        page = requests.get(url, headers=headers)  # 这里是请求网页数据了
        return page
    except Exception as e:
        time.sleep(2)
        page = requests.get(url, headers=headers)  # 这里是请求网页数据了
        return page

def getDetail(qunar_poi_id):
    url = 'https://piao.qunar.com/ticket/detail_{}.html'.format(qunar_poi_id)
    page = getPage(url)                 # 这里调用了getPage函数获取了网页数据
    # charset = page.apparent_encoding  # 网页 字符集
    selector = etree.HTML(page.text)    # 页面lxml.etree对象
    ret = selector.xpath('.//div[@class="mp-charact"]/div[@class="mp-charact-littletips"]')
    json_ret = ''
    # 获取 入园公告 和 小贴士
    if len(ret) > 0:
        filedDict = {}
        for i in range(0, len(ret)):
            titleDict = {}
            title = ret[i].xpath('.//h2[@class="mp-littletips-title pngfix"]/text()')
            titles = ret[i].xpath('.//div[@class="mp-littletips-itemtitle"]/text()')
            descs = ret[i].xpath('.//div[@class="mp-littletips-desc"]')
            for n in range(0, len(titles)):
                descslist = ""
                descs2 = descs[n].xpath('.//p/text()')
                for l in range(0, len(descs2)):
                    descslist = descslist + descs2[l]
                titleDict.setdefault(titles[n], descslist)
            filedDict.setdefault(title[0], titleDict)
            json_ret = json.dumps(filedDict, ensure_ascii=False).replace('\\', '\\\\')

    # 获取 sightId 去哪儿网景点id
    sightId = re.findall(r'\d+', selector.xpath('.//link[@rel="canonical"]/@href')[0])[0]

    # 获取评论
    recommondList = []
    bool1 = True
    for i in range(1, 3):
        if bool1 == True:
            recommond = getPage(
                'https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId={}&index={}&page={}&pageSize=10&tagType=0'.format(
                    sightId, i, i
                )).json()
            if "commentList" not in recommond['data']:
                break

            if recommond['data']['commentCount'] == 0:
                bool1 = False
                break
            else:
                recommond = recommond['data']['commentList']

            if len(recommond) > 0:
                for ii in range(0, len(recommond)):
                    if recommond[ii]['content'] != '用户未点评，系统默认好评。':
                        recommondList.append([recommond[ii]['author'], recommond[ii]['content'], recommond[ii]['date'], recommond[ii]['score'] * 2, recommond[ii]['imgs']])
                time.sleep(random.uniform(0.8, 2))
            else:
                break

    return json_ret, sightId, recommondList

def main():
    # 查出所有 景点
    with connmysql.UseMysql() as um:
        sql = "SELECT `view_id`,`qunar_id` FROM `view_extend` WHERE qunar_id is not null and label is null order by  view_id asc limit 0, 16144"
        um.cursor.execute(sql)
        data = um.cursor.fetchall()

    for i in range(0, len(data)):
        poi_id = data[i]['view_id']
        qunar_poi_id = data[i]['qunar_id']

        try:
            # 获取爬虫数据
            ret, sightId, recommondList = getDetail(qunar_poi_id)
            # 更新数据库
            with connmysql.UseMysql() as um:
                sql = "update view_extend SET `label` = '{}', `field1` = '{}', `qunar_id` = '{}' where `view_id` = {}".format(
                    1, ret, sightId, poi_id)
                um.cursor.execute(sql)
                if len(ret) != 0:
                    print(str(poi_id) + '_已获取_入园公告小贴士_成功')

                if len(recommondList) > 0:
                    wenben = 0
                    tupian = 0
                    for i in recommondList:
                        extend_field = json.dumps({'name': i[0], 'avatar': None}, ensure_ascii=False)
                        type = '文本'
                        img = []
                        if len(i[4]) > 0:
                            type = '图片'
                            for ii in i[4]:
                                img.append(ii['big'])
                            tupian  = tupian + 1
                        else:
                            wenben = wenben + 1
                        img = json.dumps(img, ensure_ascii=False).replace('\\', '\\\\')

                        sql2 = "insert into user_footprint (`view_id`, `user_id`, `type`, `content`, `media`, `state`, `addtime`, `score`, `sh`, `extend_field`) VALUES " \
                               "({}, {}, '{}', '{}', '{}', {}, '{}', {}, {}, '{}')".format(
                            poi_id, -1, type, i[1], img, 1, i[2], i[3], 1, extend_field
                        )
                        um.cursor.execute(sql2)

                    print(str(poi_id) + '_已获取_评论成功_文本评论：' + str(wenben) + '条_图片评论:' + str(tupian) + '条！')

        except Exception as e:
            print(str(poi_id) + '-----------error to update -----------------'"")
        #     print(e)
        # exit(146)
        time.sleep(random.uniform(3, 5))

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    diff = timeit.default_timer() - start
    print("总共耗时: %.6f秒" % diff)
    exit('ok')