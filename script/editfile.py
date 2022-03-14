#!/usr/bin/env python

# -*- encoding: utf-8 -*-
"""
读写文件content
"""
import codecs
import json

def makefilechange():
    path = './file/a.txt'
    file = codecs.open(path, 'r+', 'utf-8')
    list = []
    while True:
        line = file.readline()
        list.append(line.replace('\r\n', ''))
        if len(line) <= 1:
            break
    print(list)

    file.close()

def getJson():
    path = './file/camp.json'
    with open(path, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        for i in json_data['message']['data']:
            print(i)


# makefilechange()
getJson()