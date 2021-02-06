#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Author: 王小飞
@File  : count.py
@Time  : 2021/1/8 10:36
@Tool  : PyCharm
"""
from faker import Faker

# dic = {
#     "error_code": 0,
#     "stu_info":
#         [
#             {
#                 "id": 2059, "name": "小白", "sex": "男", "age": 28, "address": "河南省济源市北海大道32号",
#                 "grade": "天蝎座", "phone": "18378309272", "gold": 10896, "info":
#                 {
#                     "card": 434345432,
#                     "bank_name": '中国银行'
#                 }
#             },
#             {
#                 "id": 2067, "name": "小黑", "sex": "男", "age": 28,
#                 "address": "河南省济源市北海大道32号", "grade": "天蝎座",
#                 "phone": "12345678915", "gold": 100
#             }
#         ]
# }

# res1 = jsonpath.jsonpath(dic, '$..name')
# print(res1)
#
# res2 = jsonpath.jsonpath(dic, '$.stu_info[0].id')
# print(res2)
#
# res3 = jsonpath.jsonpath(dic, '$.stu_info[0].grade')
# print(res3)
#
# dc2 = {
#           "code": 200,
#           "data": "",
#           "message": "success"
#         }
# res4 = jsonpath.jsonpath(dc2, '$.message')
# print(res4)

# new_work_book = xlwt.Workbook()  # 创建工作簿
# new_sheet = new_work_book.add_sheet("test", cell_overwrite_ok=True)  # 创建sheet第二参数用于确认同一个cell单元是否可以重设值
# # col1 = new_sheet.col(0)
# # col1.width = 64 * 85  # 设置每列的宽度
# for co in range(3):
#     new_sheet.col(co).width = 128 * 85
#
# style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式 style
# # 设置背景颜色
# pattern = xlwt.Pattern()
# pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
# pattern.pattern_fore_colour = 17  # 给背景颜色赋值
# style.pattern = pattern  # 把背景颜色加到表格样式里去
# # 为样式创建字体
# font = xlwt.Font()
# font.name = '宋体'  # 设置字体
# font.colour_index = 0  # 设置字体颜色
# font.height = 300  # 字体大小
# font.bold = True  # 字体是否为粗体
# # font.italic = True  # 字体是否为斜体
# # font.underline = True  # 字体是否有下划线
# # font.struck_out = True  # 字体中是否有横线
# # 定义格式-字体
# style.font = font
#
# al = xlwt.Alignment()
# al.horz = 0x02  # 设置水平居中
# al.vert = 0x01  # 设置垂直居中
# style.alignment = al
#
# row_0 = ["姓名", "年龄", "性别"]  # 第一行的内容
# for m in range(0, len(row_0)):
#     new_sheet.write(0, m, row_0[m])
#     new_sheet.write(0, m, row_0[m], style)
#
# row_1 = ["第一", "第二", "第三"]  # 第二行的内容
# for m1 in range(0, len(row_1)):
#     new_sheet.write(1, m1, row_1[m1])  # 1 第几行, m1 第几列, row_1[m1] 写入的内容
#
# col1_data = ['张三', '李四', '王五']  # 第一列的内容
# for n in range(len(col1_data)):
#     new_sheet.write(n + 2, 0, col1_data[n])  # n+3 第几行, 0 第几列, col1_data[n] 写入的内容
# col2_data = [18, 19, 20]  # 第二列的内容
# for b in range(len(col2_data)):
#     new_sheet.write(b + 2, 1, col2_data[b])
# col3_data = ['男', '女', '男']  # 第三列内容
# for v in range(len(col3_data)):
#     new_sheet.write(v + 2, 2, col3_data[v])
#
# new_work_book.save("./xls/test.xls")

dct = {'account': 'string', 'password': 'string'}
china_fake = Faker("zh_CN")  # 修改本地化区域参数
us_fake = Faker("en_US")
name1 = china_fake.name()
name2 = us_fake.name()

login = list(dct.keys())

for i in login:
    if dct[i] == "string":
        dct[i] = us_fake.name()

# print(dct)

d = {
    'material':
        {
            'createTime': 'string', 'customSku': 'string', 'externalZipUri': 'string',
            'id': 0, 'isDelete': 0, 'materialGroupTemplateId': 0, 'name': 'string',
            'sku': 'string', 'thumbnailUri': 'string', 'title': 'string', 'type': 0,
            'updateTime': 'string', 'userId': 0, 'zipUri': 'string'
        },
    'materialVariants':
        [
            {
                'createTime': 'string', 'customVariantSku': 'string', 'id': 0,
                'isDelete': 0, 'materialId': 0, 'name': 'string', 'thumbnailUri': 'string',
                'title': 'string',  'updateTime': 'string', 'userId': 0, 'variantSku': 'string'
            }
        ]
}

# for key, value in d.items():
#     if isinstance(value, dict):
#         green("dict"), pink(key, value)
#         for not_nest_key, not_nest_value in value.items():
#             print(not_nest_key, not_nest_value)
#     elif isinstance(value, list):
#         green("list"), pink(key, value)
#         for nest in value:
#             for nest_key, nest_value in nest.items():
#                 print(nest_key, nest_value)
#     else:
#         raise ValueError("未定义的数据类型！")


dt3 = {
    'allowBackorders': 0,
    'barcode': 'string',
    'content':
        {
            'description': 'string',
            'id': 0,
            'seoDescription': 'string',
            'seoTitle': 'string',
            'seoUrl': 'string',
            'storeId': 0
        },
    'height': 'string',
    'id': 0,
    'inventories':
        [
            {
                'allowBackorders': 0,
                'barcode': 'string',
                'height': 'string',
                'heightUnit': 'string',
                'id': 0,
                'imageId': 0,
                'isManage': 0,
                'isSoldIndividually': 0,
                'isVirtual': 0,
                'length': 'string',
                'lengthUnit': 'string',
                'lowInventoryThreshold': 0,
                'offSaleTime': 'string',
                'productId': 0,
                'quantity': 0,
                'regularPrice': 0,
                'salePrice': 0,
                'saleTime': 'string',
                'shippingClassId': 0,
                'status': 0,
                'taxClass': 'string',
                'taxStatus': 0,
                'titleIds': 'string',
                'titleValues': 'string',
                'variantSku': 'string',
                'weight': 'string',
                'weightUnit': 'string',
                'width': 'string',
                'widthUnit': 'string'
            }
        ],
    'inventoryOriginalImage': 'string',
    'inventoryQuantity': 0,
    'inventoryStatus': 0,
    'isChargeTaxes': 0,
    'isGather': 0,
    'isManageInventory': 0,
    'isPull': 0,
    'isVirtual': 0,
    'length': 'string',
    'lowInventoryThreshold': 0,
    'name': 'string',
    'originalUrl': 'string',
    'productCategoryIds': [],
    'productGroupIds': [],
    'productImageIds': [],
    'productTagIds': [],
    'productVariantIds': [],
    'publishTime': 'string',
    'pushStatus': 0,
    'regularPrice': 0,
    'salePrice': 0,
    'sku': 'string',
    'source': 0,
    'status': 0,
    'storeId': 0,
    'taxClass': 'string',
    'taxStatus': 0,
    'taxes': 'string',
    'type': 0,
    'vendorId': 0,
    'weight': 'string',
    'width': 'string'
}

import yaml

with open("./config.yml", "r", encoding="utf-8") as config_file:
    print(yaml.load(config_file.read(), yaml.FullLoader)['url'])

