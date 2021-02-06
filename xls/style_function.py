#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Author: 王小飞
@File  : style_function.py
@Time  : 2021/1/28 15:54
@Tool  : PyCharm
"""
import xlwt


def style_customization(pattern_fore_colour, font_name, font_colour_index, font_height):
    """自定义Excel表的样式"""
    style = xlwt.XFStyle()  # 实例化样式
    font = xlwt.Font()  # 字体
    al = xlwt.Alignment()  # 对齐方式
    pattern = xlwt.Pattern()  # 背景
    borders = xlwt.Borders()  # 设置边框
    font.name = str(font_name)  # 设置字体
    font.colour_index = int(font_colour_index)  # 字体颜色
    font.height = int(font_height)  # 字体大小
    style.font = font
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = int(pattern_fore_colour)  # 设置背景颜色
    style.pattern = pattern  # 设置单元格颜色
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    style.alignment = al
    style.alignment.wrap = 1  # 自动换行
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1  # 细实线
    style.borders = borders
    return style

