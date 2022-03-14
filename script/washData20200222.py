#!/usr/bin/env python

# -*- encoding: utf-8 -*-

import os
import xlrd, xlsxwriter, re
"""
读xlsx文件
"""
def open_file(file):
    try:
        fh = xlrd.open_workbook(file)
        return fh
    except Exception as e:
        print("打开文件错误:", e)

def main1():
    mfw = xlsxwriter.Workbook('new_poi.xlsx', options={'strings_to_urls': False})  # 创建一个excel文件
    worksheet1 = mfw.add_worksheet()  # 工作表
    abcd = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    path = "G:\\code\\python_www\\file\\new_poi.xlsx"  # 待读文件
    fh = open_file(path)  # 打开
    table = fh.sheets()[0]  # 读取第一个表
    title = table.row_values(0, start_colx=0, end_colx=None)
    for ti in range(0, len(title)):
        print(title[ti])
        worksheet1.write('{}1'.format(abcd[ti]), title[ti])  # A1数据

    index = 1
    all_row = table.nrows - 2
    print(all_row)
    for oneRow in range(0, all_row):
        index = index + 1
        f = table.row_values(oneRow + 1, start_colx=0, end_colx=None)
        list35 = []
        for i in range(0, len(f)):
            if i <= 2 or i == 6:
                worksheet1.write('{}{}'.format(abcd[i], index), f[i])

            if i>= 3 and i <= 5:
                list35.append(f[i])

        list53 = []
        for i in list35:
            if len(i) != 0:
                list53.append(i)
        if len(list53) == 3:
            worksheet1.write('D{}'.format(index), list53[0])
            worksheet1.write('E{}'.format(index), list53[1])
            worksheet1.write('F{}'.format(index), list53[2])
        if len(list53) > 0 and len(list53) < 3:
            for i in list53:
                # 交通
                bool1 = i.find('公交') != -1
                bool2 = i.find('地铁') != -1
                bool3 = i.find('乘') != -1
                bool4 = i.find('车') != -1
                bool5 = i.find('驾') != -1
                bool6 = i.find('步行') != -1
                bool7 = i.find('乘') != -1
                # 票
                bool11 = i.find('票') != -1
                bool22 = i.find('人民币') != -1
                bool33 = i.find('元') != -1
                bool44 = i.find('钱') != -1
                bool55 = i.find('免费') != -1
                if bool1 or bool2 or bool3 or bool4 or bool5 or bool6 or bool7:
                    worksheet1.write('D{}'.format(index), i)
                elif bool11 or bool22 or bool33 or bool44 or bool55:
                    worksheet1.write('E{}'.format(index), i)
                else:
                    worksheet1.write('F{}'.format(index), i)

    mfw.close()

def main():
    path = "G:\\code\\python_www\\file\\new_poi.xlsx"  # 待读文件
    fh = open_file(path)  # 打开
    table = fh.sheets()[0]  # 读取第一个表
    title = table.row_values(0, start_colx=0, end_colx=None)
    for ti in range(0, len(title)):
        print(title[ti])
        worksheet1.write('{}1'.format(abcd[ti]), title[ti])  # A1数据

    index = 1
    all_row = table.nrows - 2


if __name__ == '__main__':
    main()
