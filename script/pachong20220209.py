#!/usr/bin/env python

# -*- encoding: utf-8 -*-
"""
去哪儿网数据抓取
搜索景点名称后 获取 sightId（长的那个）

"""
import common.connectMysql as connmysql
import time, requests, random, timeit
from lxml import etree  # 解析xpath网页结构


def getPage(url):  # 获取链接中的网页内容
    # 网络请求时需要包含较为完整的headers(请求头)
    # 这里的headers就是requests header的内容
    # 除了cookie 和 user-agent其他都和我的电脑一样
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'cookie': 'SECKEY_ABVK=vK3qodbdxhISdk1LV0TpbY8pfqk1MXdyLMHiJ8BjLDw%3D; BMAP_SECKEY=matWal5NcEmdTuhgWcWz9SpiVGMx6bA5pOgbbQX2mGQmRFb3-VUw6W4gJHUuRClvKrqxAuGfObyOMRI5Aq-m2aeUt79Wpnr4u8zo2tChznae22wUZhRsAFZwd9_uK3iDbsS-fot7VUJc9cinPPHIIcItceM8Fyv36RLBki0PrdxCXddnMs-tqmep58n2QxQg; QN1=00008580306c3984fc90833e; QN300=auto_4e0d874a; QN99=9247; csrfToken=nGul3vUvbuPM9neM9wFQFEnoFW8eHscy; _i=DFiEuYMzleLwGIe6-CARQ2d_jCvw; QN601=886e0cc254142ead4e52a90bd4f6fb75; QunarGlobal=10.86.213.148_-332dc806_17cc4f2acd7_-3e2d|1635391891453; QN163=0; QN48=000088002f103984fc989e11; QN667=B; QN6=auto_4e0d874a; fid=366977bf-6407-4162-a46e-406225a946d0; QN57=16353918958250.5037622739708709; ctt_june=1635411815131##iK3wVR3mauPwawPwa%3DXsXs3nEDiGWKX%3DXS2%2BaKERWK2AERDAaS2naSXNWDawiK3siK3saKjsWSP%3DaRg%3DVKX%2BWUPwaUvt; ctf_june=1635411815131##iK3waKPsWwPwawPwa%3D3wasgmXSfRWR3%3DVKvmE2PmXsa8aSfhXP3sXStAEPDniK3siK3saKjsWSP%3DaRg%3DVKXmWhPwaUvt; cs_june=f6eb45fb177ffc7b1a1adcaf4660700a27ebe6b167c763b6d541a7a193a46e3ca19d69b5c3b258949bbfc43b9d280dbc32030e943c65fb38aea06818e9299e17b17c80df7eee7c02a9c1a6a5b97c1179bb6f427eedd7e1cbd8239f6fdf39c9035a737ae180251ef5be23400b098dd8ca; QN66=auto_4e0d874a; QN69=auto_4e0d874a; QN1231=0; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; QN25=d2307eb2-c6ac-447b-b59c-dba9d7818253-9f992f90; Hm_lvt_15577700f8ecddb1a927813c81166ade=1643020797; QN71="MTI1Ljg0LjgxLjIyMjrph43luoY6MQ=="; QN277=organic; QN205=organic; QN269=24E674508A1211ECA464FA163EB096A9; QN83=qunar; Hm_lvt_872c8902458e482752d6b30a0135dcd0=1644463048; Hm_lpvt_872c8902458e482752d6b30a0135dcd0=1644463330; _vi=Oi0v1XWDS5kxMG7O2QObK5kfnLwFJskliF0vfaVsUBQ7DdPGn3GIPbhKQPfrvQBAeHgKZ66WSeetZii43dn4okEV_7h40EuYCUNXppi60tXCWmFlMM0A1MwwqZ1Kv9BtyCAzSJn1r1vNMpcXT4H_kpYOjvluFO1A7z-4S1eATIc4; QN67=456725%2C37365%2C7698%2C507738%2C457472%2C40041%2C473182%2C41794%2C469608%2C8765; QN267=113211059490b3c14c; ariaDefaultTheme=undefined; QN58=1644471103681%7C1644471784263%7C7; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1644471784; QN271=51f9f207-a580-421d-9468-3d70028ea733; JSESSIONID=0859326D6448152F97219F9581CDDC06; __qt=v1%7CVTJGc2RHVmtYMTgzSFZiZnlTbHhZQTMwV25UVTBYZGsvc0p4cFloWDkyY3dwYWJXK0VLeEczZS9vZmVEdUNzRWlPWFp0VzAyREZYSVhNWXJqa005WnAzTjlPbUMxOWRoSEFabXRpdEZIeDBoN1l6aHlpRFkyUUxUSWdrVThRbUNyM1puMjgvMExQc2Q4RGJ0N2pYcGlVTm5Da3JJa0VEL0xQSWg2QzByOHNnPQ%3D%3D%7C1644471854245%7CVTJGc2RHVmtYMStvK2xLbGFXa3UzZkdPczNvZUNmaklVZlFHUEZNUXN6UEtINVJ5b0g0ME02ZjBzV1IzMFdyeFVKN1pPQkhJSWhmTkR3NlAwaDFtZkE9PQ%3D%3D%7CVTJGc2RHVmtYMTlWSmlVd2o4bVZ0SkZjbHN6Yy9iNjJDS05uRmpBT2h0UWMzdHhsM2ZJSDlBeFhVejZMeUcvdkVMV1pKQkQ0bVNHMFlLcndFeWZOTGJFTGs5ZnFWcUtYYkNxWG4wZ05xV0thUCtvMG4vN1BOeW95bTBoWmNkR3pIM2pOUm83cW9FdlhFemU0L3BiTlR5Tjh0Y2ZGUmwrZUxMUSt5ZzNkUkI4MHUxZys5cVEvYWEycnQ5d00vWDIxM010TWlQODZDd3ExVWtnSUxQUUFMV01KYVV0a2RsSWFIOGEveHd4Q2dQa1RvWk1SYlR6ZVFsbjBGdm5pOGZDd2hYU3FMNElLMmhyZFVWQkZNQVJvQjBtd05tWlZLTVRtYjA4U0toMjF4cW5sWGtsYzVpb0xoc2JDOFo0UXNjODFTb1NvRmNqYVNyVkxudys3YnBvUE40UXNxUjBJTXN5eG8wYkZ1R1dkQ21hcnI3UllMMW5iaW5VRHFKajdXVVVDRHBlLzdMKys0NVlJRmpRQTAzQXdpNENwQUZrNE9rd0F1UUZJUWpJYlNlS2ZlSUttL1pldFp4R0xlRDN0dTB1OXVEUmp6TW44bFZHVzdhVUdvNTc0V29SZkYybHVHcGVZWnJVdkR6SnpFTmpZdnBGRmkyUGJMQXNob0gxSmZXZ2sxWEJNeVFjbmxBeEJySzFPb2EvU0s0eW1oS1FhYWEwaEZUTFA5RElJKy8wa2hYSlJSWTdNZ3ZwVE5jamhjSDNPTHoxR1ZYeHpxSGF5MGZOVVkvRlpEeTNRTGpGSTN5dzhnbkdEQWZEWll4YTcraU9sbFY1NldSazdBQ2RxbThqOEphVEJxM0lDallwK2pSN0ZSZXJJbXpudXZRZU1QdkRsTkhnT1hMUzBiOFBuZ3VUdEltMjl4Qm1wMHVLa1dBZ2hQM0hHS2kyamQ3dW85dTJLeG54ek1TdlJTMVVrYm0vblQ1bUsvR3VWZGkrUURML2dpRHVrQy8rTkd5OXYxa0RmL2wwdm1VRDVqcGhXcnFWNWxxVTRFdz09; QN63=%E9%87%8D%E5%BA%86%7C%E6%83%85%E4%BA%BA%E6%A0%91%7C%E9%A6%99%E6%A0%BC%E9%87%8C%E6%8B%89%E5%A4%A7%E5%B3%A1%E8%B0%B7%E5%B7%B4%E6%8B%89%E6%A0%BC%E5%AE%97%7C%E5%A4%A7%E4%B8%B0%E4%B8%8A%E6%B5%B7%E7%9F%A5%E9%9D%92%E7%BA%AA%E5%BF%B5%E9%A6%86%7C%E5%8C%97%E4%BA%AC%7C%E4%B8%8A%E6%B5%B7%E8%BF%AA%E5%A3%AB%E5%B0%BC%7C%E4%B8%9C%E6%A1%A5%E9%92%9F%E9%BC%93%E5%AF%A8%7C%E6%AD%A6%E5%AE%81%E9%B2%81%E6%BA%AA%E6%B4%9E%7C%E4%B8%8A%E6%B5%B7%E6%B5%B7%E6%98%8C%E6%B5%B7%E6%B4%8B%E5%85%AC%E5%9B%AD',
        'Host': 'piao.qunar.com',
        'Referer': 'https://piao.qunar.com/ticket/list.htm?keyword=%E6%83%85%E4%BA%BA%E6%A0%91&region=&from=mpl_search_suggest',
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

def getList(keyword):
    url = 'https://piao.qunar.com/ticket/list.htm?keyword={}&region=&from=mpl_search_suggest'.format(keyword)
    page = getPage(url)                 # 这里调用了getPage函数获取了网页数据
    # charset = page.apparent_encoding  # 网页 字符集
    selector = etree.HTML(page.text)    # 页面lxml.etree对象
    qunar_poi_id = selector.xpath('.//div[@class="search_result"]//@data-id')[0]
    return qunar_poi_id

def main():
    # 查出所有 景点
    with connmysql.UseMysql() as um:
        sql = "SELECT `id`,`name`,`version` FROM `view_list` WHERE version = 0 order by  id asc limit 0, 16144"
        um.cursor.execute(sql)
        data = um.cursor.fetchall()

    for i in range(0, len(data)):
        now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        poi_id = data[i]['id']
        poi_name = data[i]['name']
        try:
            # 获取爬虫数据
            qunar_poi_id = getList(poi_name)
            # 更新数据库
            with connmysql.UseMysql() as um:
                version = data[i]['version'] + 1
                sql1 = "update view_list SET `version` = {}, `updtime` = '{}' where `id` = {}".format(
                    version, now_date, poi_id)
                sql2 = "update view_extend SET `qunar_id` = {} where `view_id` = {}".format(
                    qunar_poi_id, poi_id)
                um.cursor.execute(sql1)
                um.cursor.execute(sql2)
                print(str(data[i]['name']) + '_已获取到去哪详情id')
        except Exception as e:
            print(str(data[i]['name']) + '-----------error to update -----------------'"")
        time.sleep(random.uniform(1, 3))

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    diff = timeit.default_timer() - start
    print("总共耗时: %.6f秒" % diff)
    exit('ok')