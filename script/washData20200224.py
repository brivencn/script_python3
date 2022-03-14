#!/usr/bin/env python

# -*- encoding: utf-8 -*-

import os
import pandas as pd
import xlrd, xlsxwriter, re, json, numpy
import common.connectMysql as connmysql
"""
2个xlsx文件 其中一个文件内容对应的列 替换另一个文件内容对应的列
"""
def main():
    # 查出所有 景点
    with connmysql.UseMysql() as um:
        sql = "SELECT `id`, `name` FROM `view_list` WHERE attribute = '自驾景点' order by  id asc"
        um.cursor.execute(sql)
        data = um.cursor.fetchall()
    allPoi = pd.DataFrame(data)
    xl1 = pd.read_excel("G:\\code\\python_www\\file\\workbook1.xlsx")  # 数据
    list_xl1 = xl1.values.tolist()  # 转list
    for i in list_xl1:
        view_name = i[6]
        view_id = allPoi[allPoi.name == view_name].values.tolist()[0][0]
        fields = ['phone', 'poi_url', 'paytime', 'traffic', 'tickt', 'open_info2']
        print(i)
        print(view_id)
        for e in range(0, 6):
            if pd.isnull(i[e]) is False:
                with connmysql.UseMysql() as um:
                    sql = "UPDATE view_extend SET `{}` = '{}' WHERE `view_id` = {}".format(fields[e], i[e], view_id)
                    print(sql)
                    um.cursor.execute(sql)

def main1():
    xl1 = pd.read_excel("G:\\code\\python_www\\file\\new_poi.xlsx")  # 数据
    list_xl1 = xl1.values.tolist()  # 转list
    xl2 = pd.read_excel("G:\\code\\python_www\\file\\小时.xlsx")  # 小时
    # print(xl1, xl2)
    # print(xl2.values)
    # print(type(xl2.values.tolist()))
    # print(xl1.index)
    # print(xl1.columns)
    title = xl1.columns.tolist()
    用时参考 = xl1['用时参考']
    # print(用时参考)
    # print('-'*30)
    # print(用时参考[pd.isnull(xl1.用时参考)])

    # exit(1)
    # print(xl2.dtypes)
    # print(xl2.size)
    # print(xl2.ndim)
    # print(xl2.shape)
    for i in xl2.values:
        list1 = i.tolist()
        # print(list1[0], '*'*30, list1[1])
        item1 = 用时参考[xl1.用时参考 == list1[0]]
        # print(item1, '+'*30, len(item1.index.tolist()))
        list_item1 = item1.index.tolist()
        # print(list_item1)
        for e in list_item1:
            # print(list_xl1[e][2])
            list_xl1[e][2] = list1[1]

    # print(list_xl1)
    mfw = xlsxwriter.Workbook('workbook1.xlsx', options={'strings_to_urls': False})  # 创建一个excel文件
    worksheet1 = mfw.add_worksheet()  # 工作表
    abcd = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for ti in range(0, len(title)):
        worksheet1.write('{}1'.format(abcd[ti]), title[ti])  # A1数据

    index = 1
    for row in range(0, len(list_xl1)):
        index = index + 1
        for col in range(0, len(list_xl1[row])):
            val = None if pd.isnull(list_xl1[row][col]) else list_xl1[row][col]
            worksheet1.write('{}{}'.format(abcd[col], index), val)

    mfw.close()


if __name__ == '__main__':
    main()
