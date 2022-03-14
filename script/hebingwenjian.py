import os
import xlrd, xlsxwriter
"""
合并xlsx文件
"""
def get_files(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件
        return files

def open_file(file):
    try:
        fh = xlrd.open_workbook(file)
        return fh
    except Exception as e:
        print("打开文件错误:", e)

def get_file_v(file_name, sheet_num):
    rvalue = []
    fh = open_file(file_name)
    sheet = fh.sheets()[sheet_num]
    row_num = sheet.nrows
    for item in range(0, row_num):
        rvalue.append(sheet.row_values(item))
    return rvalue

def excel_implode(files, path):
    end_xls = "去哪儿网_全国34省份景区.xlsx"
    all_xls = files
    all_conent = []
    for i in range(0, len(files)):
        file_name = "{}\\{}".format(path, files[i])
        file = open_file(file_name)
        file_sheet = file.sheets()
        file_value = get_file_v(file_name, 0)
        if (i == 0):
            all_conent.append(file_value[0])
        for ii in range(1, len(file_value)):
            all_conent.append(file_value[ii])

    row = 0
    endxls = xlsxwriter.Workbook(end_xls)
    end_xlsx_sheet = endxls.add_worksheet("sheet")
    for sheet in all_conent:
        row += 1
        col = 0
        for sheetcol in sheet:
            end_xlsx_sheet.write(row, col, sheetcol)
            col += 1

    endxls.close()


def main():
    path = "D:\\Python\\pythonProject\\国内景点"
    files = get_files(path)
    if len(files):
        excel_implode(files, path)
        print("code finished")
    else:
        print("not found files")

if __name__ == '__main__':
    main()