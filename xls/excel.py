#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Author: 王小飞
@File  : excel.py
@Time  : 2021/1/10 10:03
@Tool  : PyCharm
"""
import xlwt
import xlrd
from xlutils.copy import copy
from time import strftime
from getBaseData import *
from style_function import style_customization


class SwaggerData:
    """初始文件"""
    def __init__(self, file_path, first_col_data, sheets, all_data):
        self.filePath, self.firstColData, self.Sheets = file_path, first_col_data, sheets
        self.workBook = xlwt.Workbook()
        for sh in self.Sheets:
            try:
                no_support = ['/', '?', '*', "\\"]  # excel创建sheet表单时不支持的特殊字符
                for nos in no_support:
                    if nos in sh:
                        sh = sh.replace(nos, "-")  # 将特殊字符替换成 -
                self.Sheet = self.workBook.add_sheet(sh, cell_overwrite_ok=True)
            except BaseException as err:
                raise err

            if isinstance(self.firstColData, list):
                for col in range(len(self.firstColData)):
                    self.Sheet.col(col).width = 128 * 85
                style = style_customization(
                    pattern_fore_colour=17, font_name="微软雅黑",
                    font_colour_index=0, font_height=300
                )
                for row in range(len(self.firstColData)):
                    self.Sheet.write(0, row, self.firstColData[row], style)
            else:
                raise TypeError("数据类型错误，需要list")

            if isinstance(all_data, list):
                for num, data in enumerate(all_data):
                    n = num+1
                    for i in range(len(data)):
                        if data[0] == sh:
                            if isinstance(data[i], dict):
                                self.Sheet.write(n, i, str(data[i]))  # 转为字符串
                            elif isinstance(data[i], list):
                                self.Sheet.write(n, i, str(data[i]))
                            else:
                                self.Sheet.write(n, i, data[i])
            else:
                raise TypeError("数据类型错误，需要list")
        self.workBook.save(self.filePath)


def remove_empty_lines(first_col_data, initial_file_path, new_file_path):
    """读取初始文件并删除空白行"""
    work_book = xlrd.open_workbook(initial_file_path, formatting_info=True)
    sheet_name = work_book.sheet_names()
    new_book = xlwt.Workbook()
    for sheet in sheet_name:
        new_sheet = new_book.add_sheet(sheetname=sheet, cell_overwrite_ok=True)
        work_sheet = work_book.sheet_by_name(sheet)
        rows = work_sheet.nrows
        row_0 = first_col_data
        sheet_list = []  # 每一行的数据 work_sheet.row_values(row) for row in range(1, rows)
        n = 1  # 每个sheet的开始写入行
        for row in range(rows):
            r = work_sheet.row_values(row)
            if r[0] == "" or r[0] == "模块":
                pass
            else:
                if r[0] == sheet:
                    sheet_list.append(r)
        for row_1 in sheet_list:
            """------------标题行的设置-------------"""
            for co in range(len(row_0)):  # 初始的列宽
                new_sheet.col(co).width = 56 * 85
            new_sheet.col(3).width, new_sheet.col(6).width = 128 * 85, 224 * 85  # 单独设置的列宽
            new_sheet.col(7).width, new_sheet.col(9).width = 288 * 85, 128 * 85
            style = style_customization(
                pattern_fore_colour=17, font_name="微软雅黑",
                font_colour_index=0, font_height=350
            )
            for m in range(0, len(row_0)):
                new_sheet.write(0, m, row_0[m]), new_sheet.write(0, m, row_0[m], style)
            """----------去除空行后的内容 设置样式--------------"""
            style_1 = style_customization(
                pattern_fore_colour=42, font_name="微软雅黑",
                font_colour_index=64, font_height=200
            )
            for k in range(0, len(row_1)):
                new_sheet.write(n, k, row_1[k], style_1)
            n += 1
    new_book.save(new_file_path)


def file_compare(new_file_path, old_file_path, copy_file_path):
    """对比Excel文件: new_file_path:新生成的文件, old_file_path：需要对比的文件；copy_file_path：对比后的文件保存路径"""
    new_book = xlrd.open_workbook(new_file_path, formatting_info=True)
    old_book = xlrd.open_workbook(old_file_path, formatting_info=True)
    new_sheets, old_sheets = new_book.sheet_names(), old_book.sheet_names()  # 新文件的所有sheet 旧文件的所有sheet
    new_list, old_list = [new for new in new_sheets], [old for old in old_sheets]  # 新文件和旧文件的所有sheet
    copy_book = copy(old_book)  # 复制旧文件
    sheet_index = 0  # sheet表的下标
    more_old = []
    blue(f"新文件有{len(new_list)}张表；旧文件有{len(old_list)}张表")
    if len(new_list) == len(old_list):  # 如果新的表数量和旧的相等
        for new_sh, old_sh in zip(new_list, old_list):
            sheet_index += 1
            if new_sh == old_sh:
                cop_sheet = copy_book.get_sheet(sheet_index-1)  # cop过来的表
                new_sheet, old_sheet = new_book.sheet_by_name(new_sh), old_book.sheet_by_name(old_sh)  # 新的和旧的sheet表
                new_rows, old_rows = new_sheet.nrows, old_sheet.nrows  # 新sheet和旧sheet的最大行数
                new_data_list = [new_sheet.row_values(new_row) for new_row in range(1, new_rows)]  # 去除标题行，从1开始遍历
                old_data_list = [old_sheet.row_values(old_row) for old_row in range(1, old_rows)]
                if new_rows > old_rows:  # 如果新文件的sheet表中的行数比旧的sheet表行数多
                    old_case_id = [old_[1] for old_ in old_data_list]  # 当前sheet标的所有用例ID
                    for new_data in new_data_list:
                        if new_data[1] not in old_case_id:  # 如果新sheet表中的用例ID不在旧sheet表中的用例ID列表
                            for row in range(old_rows, new_rows):  # 行数，旧表的最大行开，新表的最大行结束
                                for col, data in enumerate(new_data):  # 新表比旧表多出的数据
                                    """----------设置样式，字体-------"""
                                    style = style_customization(
                                        pattern_fore_colour=26, font_name="微软雅黑",
                                        font_colour_index=64, font_height=200
                                    )
                                    cop_sheet.write(row, col, data, style)
                elif new_rows < old_rows:
                    red(f"新的：{new_sh}表 {new_rows}行，旧的{old_rows}行")

    elif len(new_list) > len(old_list):  # 新文件的sheet比旧文件的多
        red("新表数量比旧表多！!")
        for new_sh in new_list:
            if new_sh not in [old2.replace("skip-", "") for old2 in old_sheets]:
                copy_book.add_sheet(new_sh)
                cop_sheet = copy_book.get_sheet(len(new_list) - 1)  # cop过来的表
                new_sheet = new_book.sheet_by_name(new_sh)
                new_data_list = [new_sheet.row_values(new_row) for new_row in range(new_sheet.nrows)]
                cop_sheet.col(3).width, cop_sheet.col(6).width = 128 * 85, 224 * 85  # 单独设置的列宽
                cop_sheet.col(7).width, cop_sheet.col(9).width = 288 * 85, 128 * 85
                for row, new_data in enumerate(new_data_list):
                    for col, data in enumerate(new_data):
                        style = style_customization(
                            pattern_fore_colour=42, font_name="微软雅黑",
                            font_colour_index=64, font_height=200
                        )
                        cop_sheet.write(row, col, data, style)

    elif len(new_list) < len(old_list):  # 新文件的sheet比旧文件的少
        red("旧表数量比新表多！！")
        for old_sh in old_list:
            old_sh = old_sh.replace("skip-", "")
            if old_sh not in [new2 for new2 in new_sheets]:
                more_old.append(old_sh)

    else:
        raise ValueError("参数错误！")

    if more_old:
        pink(f"旧文件比新文件多出的表：\n{more_old}")

    copy_book.save(copy_file_path)


if __name__ == '__main__':
    print(strftime("%Y-%m-%d_%H-%M-%S"))
    file_compare(
        new_file_path="./new_data/erp-api.xls",
        old_file_path="./old_data/erp-api.xls",
        copy_file_path=f"./old_data/erp-api.xls"
    )
