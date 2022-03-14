#!/usr/bin/env python

# -*- encoding: utf-8 -*-

import os
import xlrd, xlsxwriter, re, pandas, json
import common.connectMysql as connmysql
"""
读xlsx文件 写入数据库
"""
def open_file(file):
    try:
        fh = xlrd.open_workbook(file)
        return fh
    except Exception as e:
        print("打开文件错误:", e)

# def main():
#     mfw = xlsxwriter.Workbook('new_poi.xlsx', options={'strings_to_urls': False})  # 创建一个excel文件
#     worksheet1 = mfw.add_worksheet()  # 工作表
#     abcd = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
#             'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
#
#     path = "G:\\code\\python_www\\file\\poi.xlsx"  # 待读文件
#     fh = open_file(path)  # 打开
#     table = fh.sheets()[0]  # 读取第一个表
#     title = table.row_values(0, start_colx=0, end_colx=None)
#     for ti in range(0, len(title)):
#         print(title[ti])
#         worksheet1.write('{}1'.format(abcd[ti]), title[ti])  # A1数据
#
#     index = 1
#     all_row = table.nrows - 1
#     list1 = []
#     for oneRow in range(0, all_row):
#         f = table.row_values(oneRow + 1, start_colx=0, end_colx=None)
#         if list1.count(f[6]) == 0:
#             index = index + 1
#             list1.append(f[6])
#             for i in range(0, len(f)):
#                 worksheet1.write('{}{}'.format(abcd[i], index), f[i])
#     mfw.close()

def main():
    # 查出所有 景点
    with connmysql.UseMysql() as um:
        sql = "SELECT `id`, `name` FROM `view_list` WHERE attribute = '自驾景点' order by  id asc"
        um.cursor.execute(sql)
        data = um.cursor.fetchall()

    allPoi = pandas.DataFrame(data)

    mfw = xlsxwriter.Workbook('new_printfoot.xlsx', options={'strings_to_urls': False})  # 创建一个excel文件
    worksheet1 = mfw.add_worksheet()  # 工作表
    abcd = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    worksheet1.write('A1', 'view_id')
    worksheet1.write('B1', 'user_id')
    worksheet1.write('C1', 'type')
    worksheet1.write('D1', 'content')
    worksheet1.write('E1', 'media')
    worksheet1.write('F1', 'state')
    worksheet1.write('G1', 'version')
    worksheet1.write('H1', 'addtime')
    worksheet1.write('I1', 'updtime')
    worksheet1.write('J1', 'score')
    worksheet1.write('K1', 'route_id')
    worksheet1.write('L1', 'location')
    worksheet1.write('M1', 'location_name')
    worksheet1.write('N1', 'delete')
    worksheet1.write('O1', 'notice')
    worksheet1.write('P1', 'sh')
    worksheet1.write('Q1', 'extend_field')
    worksheet1.write('R1', 'origin')

    path = "G:\\code\\python_www\\file\\printfoot.xlsx"  # 待读文件
    fh = open_file(path)  # 打开
    table = fh.sheets()[0]  # 读取第一个表

    all_row = table.nrows - 1
    index = 1
    user_id = -1
    score = 10
    state = 1
    version = 0
    origin = '马蜂窝'
    for oneRow in range(0, all_row):
        f = table.row_values(oneRow + 1, start_colx=0, end_colx=None)
        print(f)
        if len(str(f[1])) == 0 or len(str(f[2])) == 0 or len(str(f[3])) == 0:
            continue
        index = index + 1
        imgs = []
        for i in [f[4], f[5], f[6], f[7]]:
            if len(i) > 0:
                tempi = i.split("?imageMo")
                imgs.append(tempi[0])
        if len(imgs) > 0:
            type = '图片'
        else:
            type = '文本'

        id = allPoi[allPoi.name == f[0]].id
        for i in id.index:
            id = id.get(i)

        avatar = f[2].split("?imageMo")
        extend_field = json.dumps({"name": f[1], "avatar": avatar[0]}, ensure_ascii=False)
        imgs = json.dumps(imgs, ensure_ascii=False).replace('\\', '\\\\')
        worksheet1.write('A{}'.format(index), id)
        worksheet1.write('B{}'.format(index), user_id)
        worksheet1.write('C{}'.format(index), type)
        worksheet1.write('D{}'.format(index), f[3])
        worksheet1.write('E{}'.format(index), imgs)
        worksheet1.write('F{}'.format(index), state)
        worksheet1.write('G{}'.format(index), version)
        worksheet1.write('H{}'.format(index), f[8])
        worksheet1.write('I{}'.format(index), None)
        worksheet1.write('J{}'.format(index), score)
        worksheet1.write('K{}'.format(index), None)
        worksheet1.write('L{}'.format(index), None)
        worksheet1.write('M{}'.format(index), None)
        worksheet1.write('N{}'.format(index), 0)
        worksheet1.write('O{}'.format(index), 0)
        worksheet1.write('P{}'.format(index), 1)
        worksheet1.write('Q{}'.format(index), extend_field)
        worksheet1.write('R{}'.format(index), origin)

    mfw.close()

if __name__ == '__main__':
    main()
