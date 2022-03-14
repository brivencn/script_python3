#!/usr/bin/env python

# -*- encoding: utf-8 -*-
import requests, re

def download_img(img_url, name):
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        ret = open('G:\\file\\camp_img\\' + name, 'wb').write(r.content)  # 将内容写入图片
    else:
        ret = 0
    del r
    return ret

if __name__ == '__main__':
    # 下载要的图片
    img_url = "https://imgs.qunarzz.com/sight/p0/1708/d2/d24ec25a792e34a5a3.img.jpg_710x360_7bfb406d.jpg"
    img = re.sub(r'_710x360+.*', '', img_url)
    print(img)
    name = "a.jpg"
    print(download_img(img_url, name))
