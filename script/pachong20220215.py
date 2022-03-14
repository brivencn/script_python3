#!/usr/bin/env python

# -*- encoding: utf-8 -*-
"""
马蜂窝数据获取

"""
import common.connectMysql as connmysql
import time, requests, re, random, timeit, json, urllib.parse
from lxml import etree  # 解析xpath网页结构


def getPage(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'Connection': 'keep-alive',
        'cookie': 'SECKEY_ABVK=4sIvRFtS/J+ARFTm3aNNav6g6Rvvvk0AtqoOBV5wi3g%3D; BMAP_SECKEY=lhS1EnvYoNrG-VQXZvsG4yG0ycHv23XUA14jst2aR_ITZg-htfOyKdplY5YSehIkKA9tp0D2onchnR3AJ8tPS2rIPy2oJHTGyUTd6BoG-NTXMlZugCqW6r_zOKDbCnZoJajKDo4g17Cyry2asMHfsGd4Q37yNDz34i6M7tFpK7KAqWWDrp12jk_-fsBzMxdi; __jsluid_s=d1138135a3924f73eeee5ac597e246a1; PHPSESSID=cc944toniicc118mgh9425dnp5; mfw_uuid=620c6e27-d1be-e88b-bd67-1d6e4ac6d29e; __jsluid_h=42e4d764884dea3d3083a14a556cfa33; UM_distinctid=17f008e4cc248c-050fba02f5fdcd-f791539-1fa400-17f008e4cc31412; uva=s%3A221%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1644981799%3Bs%3A10%3A%22last_refer%22%3Bs%3A152%3A%22http%3A%2F%2Fwww.mafengwo.cn%2Fsearch%2Fq.php%3Fq%3D%25E4%25B8%258A%25E6%25B5%25B7%25E8%25BF%25AA%25E5%25A3%25AB%25E5%25B0%25BC%25E4%25B9%2590%25E5%259B%25ADsadasdasd%26seid%3DAB22E473-650F-4BB3-B588-6DFC6C36B8D5%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1644981799%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=620c6e27-d1be-e88b-bd67-1d6e4ac6d29e; __omc_chl=; mfw_passport_redirect=https%3A%2F%2Fwww.mafengwo.cn%2Fpoi%2F9043133.html; _r=baidu; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A18%3A%22www.baidu.com%2Flink%22%3Bs%3A1%3A%22t%22%3Bi%3A1645060655%3B%7D; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A21%3A%22https%3A%2F%2Fwww.baidu.com%22%3Bs%3A2%3A%22hp%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A1026%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222022-02-17+09%3A17%3A35%22%3B%7D; __mfwothchid=referrer%7Cwww.baidu.com; __mfwc=referrer%7Cwww.baidu.com; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1644458338,1645060656,1645060664; bottom_ad_status=0; __omc_r=; ariaReadtype=1; ariaoldFixedStatus=false; ariaStatus=false; __mfwa=1644981800017.57865.9.1645078212149.1645082222475; __mfwlv=1645083506; __mfwvn=7; __jsl_clearance_s=1645083887.617|0|p5vMKdc8ytZOBa1%2BGkZoHJEIdXk%3D; CNZZDATA30065558=cnzz_eid%3D760155744-1644978276-http%253A%252F%252Fwww.mafengwo.cn%252F%26ntime%3D1645079187; __mfwb=312c550979e6.5.direct; __mfwlt=1645083906; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1645083907',
        'Host': 'www.mafengwo.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://www.mafengwo.cn/search/q.php?q=%E4%B8%8A%E6%B5%B7%E8%BF%AA%E5%A3%AB%E5%B0%BC%E4%B9%90%E5%9B%ADsadasdasd&seid=AB22E473-650F-4BB3-B588-6DFC6C36B8D5',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }
    try:
        page = requests.get(url, headers=headers)  # 这里是请求网页数据了
        return page
    except Exception as e:
        time.sleep(2)
        page = requests.get(url, headers=headers)  # 这里是请求网页数据了
        return page

def getPage2(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'Connection': 'keep-alive',
        'cookie': 'SECKEY_ABVK=4sIvRFtS/J+ARFTm3aNNav6g6Rvvvk0AtqoOBV5wi3g%3D; BMAP_SECKEY=lhS1EnvYoNrG-VQXZvsG4yG0ycHv23XUA14jst2aR_ITZg-htfOyKdplY5YSehIkKA9tp0D2onchnR3AJ8tPS2rIPy2oJHTGyUTd6BoG-NTXMlZugCqW6r_zOKDbCnZoJajKDo4g17Cyry2asMHfsGd4Q37yNDz34i6M7tFpK7KAqWWDrp12jk_-fsBzMxdi; __jsluid_s=d1138135a3924f73eeee5ac597e246a1; PHPSESSID=cc944toniicc118mgh9425dnp5; mfw_uuid=620c6e27-d1be-e88b-bd67-1d6e4ac6d29e; __jsluid_h=42e4d764884dea3d3083a14a556cfa33; UM_distinctid=17f008e4cc248c-050fba02f5fdcd-f791539-1fa400-17f008e4cc31412; uva=s%3A221%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1644981799%3Bs%3A10%3A%22last_refer%22%3Bs%3A152%3A%22http%3A%2F%2Fwww.mafengwo.cn%2Fsearch%2Fq.php%3Fq%3D%25E4%25B8%258A%25E6%25B5%25B7%25E8%25BF%25AA%25E5%25A3%25AB%25E5%25B0%25BC%25E4%25B9%2590%25E5%259B%25ADsadasdasd%26seid%3DAB22E473-650F-4BB3-B588-6DFC6C36B8D5%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1644981799%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=620c6e27-d1be-e88b-bd67-1d6e4ac6d29e; __omc_chl=; mfw_passport_redirect=https%3A%2F%2Fwww.mafengwo.cn%2Fpoi%2F9043133.html; _r=baidu; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A18%3A%22www.baidu.com%2Flink%22%3Bs%3A1%3A%22t%22%3Bi%3A1645060655%3B%7D; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A21%3A%22https%3A%2F%2Fwww.baidu.com%22%3Bs%3A2%3A%22hp%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A1026%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222022-02-17+09%3A17%3A35%22%3B%7D; __mfwothchid=referrer%7Cwww.baidu.com; __mfwc=referrer%7Cwww.baidu.com; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1644458338,1645060656,1645060664; bottom_ad_status=0; __omc_r=; ariaReadtype=1; ariaoldFixedStatus=false; ariaStatus=false; __mfwa=1644981800017.57865.9.1645078212149.1645082222475; __mfwlv=1645083506; __mfwvn=7; __jsl_clearance_s=1645083887.617|0|p5vMKdc8ytZOBa1%2BGkZoHJEIdXk%3D; CNZZDATA30065558=cnzz_eid%3D760155744-1644978276-http%253A%252F%252Fwww.mafengwo.cn%252F%26ntime%3D1645079187; __mfwb=312c550979e6.5.direct; __mfwlt=1645083906; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1645083907',
        'Host': 'www.mafengwo.cn',
        'Pragma': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }
    try:
        page = requests.get(url, headers=headers)  # 这里是请求网页数据了
        return page
    except Exception as e:
        time.sleep(2)
        page = requests.get(url, headers=headers)  # 这里是请求网页数据了
        return page

def getDetail(name):
    url = 'http://www.mafengwo.cn/search/q.php?q={}'.format(name)
    page = getPage(url)                 # 这里调用了getPage函数获取了网页数据

    # charset = page.apparent_encoding  # 网页 字符集
    selector = etree.HTML(page.text)    # 页面lxml.etree对象
    ret = selector.xpath('.//div[@class="search-mdd-wrap"]/a/@href')
    mafengwoid = 0
    url = ""
    if len(ret) > 0:
        '''如有有获取到数据
        '''
        url = ret[0]
        ret = urllib.parse.parse_qs(urllib.parse.urlparse(ret[0]).query)
        mafengwoid = ret['id'][0]


    return mafengwoid, url

def getDetail2(mafengwoid):
    url = 'https://www.mafengwo.cn/poi/{}.html'.format(mafengwoid)
    page = getPage2(url)                 # 这里调用了getPage函数获取了网页数据
    # charset = page.apparent_encoding  # 网页 字符集
    selector = etree.HTML(page.text)    # 页面lxml.etree对象
    poi_name = selector.xpath('.//div[@class="title"]/h1/text()') # 景点名称
    head = selector.xpath('//div[@class="head-logo"]/*')
    if len(head) == 0:
        return False

    jianyiyongshi = selector.xpath('//ul[@class="baseinfo clearfix"]/li[@class="item-time"]/div[@class="content"]/text()') # 建议时长
    phone = selector.xpath('//ul[@class="baseinfo clearfix"]/li[@class="tel"]/div[@class="content"]/text()') # 景区电话
    introduction_info2 = selector.xpath('//div[@class="mod mod-detail"]/div[@class="summary"]/text()')  # 景区详情页
    poi_url = selector.xpath('//ul[@class="baseinfo clearfix"]/li[@class="item-site"]/div[@class="content"]/text()') # 景区网址
    menpiaokaifangshijianetree = selector.xpath('//div[@class="mod mod-detail"]/dl')  # 景区详情页
    menpiaokaifangshijian = {}
    for i in menpiaokaifangshijianetree:
        title = i.xpath('.//dt/text()')[0]
        content = i.xpath('./dd/div/text()')
        if len(content) == 0:
            content = i.xpath('./dd/text()')
        menpiaokaifangshijian.setdefault(title, content)
    json_ret = json.dumps(menpiaokaifangshijian, ensure_ascii=False).replace('\\', '\\\\')

    return [poi_name[0] if len(poi_name) > 0 else "", jianyiyongshi[0] if len(jianyiyongshi) > 0 else "",\
    phone[0] if len(phone) > 0 else "", introduction_info2[0] if len(introduction_info2) > 0 else "", \
    poi_url[0] if len(poi_url) > 0 else "", json_ret]

def main():
    # 查出所有 景点
    with connmysql.UseMysql() as um:
        sql = "SELECT a.`name`, b.`view_id` FROM `view_extend` as b LEFT JOIN `view_list` as a ON a.`id` = b.`view_id`  WHERE b.label is not null order by  b.view_id asc"
        um.cursor.execute(sql)
        data = um.cursor.fetchall()

    for i in data:

        try:
            # 获取马蜂窝POIid
            mafengwoid, url = getDetail(i['name'])
            if mafengwoid != 0:
                # 获取马蜂窝详情页
                ret2 = getDetail2(mafengwoid)
                if ret2 == False:
                    print('cookie过期请更新')
                    break
                with connmysql.UseMysql() as um:
                    sql = "update view_extend SET `label` = null, `phone` = '{}', `mafengwo_id` = '{}', `paytime` = '{}', `mafengwo_name` = '{}', `introduction_info2` = '{}', `poi_url` = '{}' \
                                        ,`field2` = '{}'  where `view_id` = {}".format(
                        ret2[2], mafengwoid, ret2[1], ret2[0], ret2[3], ret2[4], ret2[5], i['view_id'])
                    um.cursor.execute(sql)
                    print(str(i['view_id']) + '__' + i['name'] + '_获取成功' + str(mafengwoid))
            else:
                with connmysql.UseMysql() as um:
                    sql = "update view_extend SET `label` = null where `view_id` = {}".format(i['view_id'])
                    um.cursor.execute(sql)
                print(str(i['view_id']) + '__' + i['name'] + '-----------mafengwoid error to update -----------------')
        except Exception as e:
            print(str(i['view_id']) + '__' + i['name'] + '-----------error to update -----------------')

        # 循环间隙
        time.sleep(random.uniform(2, 5))

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    diff = timeit.default_timer() - start
    print("总共耗时: %.6f秒" % diff)
    exit('ok')