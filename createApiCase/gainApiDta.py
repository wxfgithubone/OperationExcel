#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Author: 王小飞
@File  : gainApiDta.py
@Time  : 2021/1/13 15:42
@Tool  : PyCharm
"""
import xlrd
import os
from commonApi import CommonApi


header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        " (KHTML, like Gecko)Chrome/84.0.4147.105 Safari/537.36",
          "Content-Type": "application/json"}


class GainApiData(object):
    """获取出接口用例"""

    def __init__(self, file_name, sheet):
        path = fr"E:\Desktop\ParsSwagger\xls\old_data\{file_name}"
        if os.path.exists(path):
            self.workBook = xlrd.open_workbook(path, formatting_info=True)
        else:
            raise FileNotFoundError("文件未找到！")
        self.adminBseUrl = "http://api.admin.shopmell.com"
        self.erpBaseUrl = "http://api.erp.shopmell.com"
        self.supplierBaseUrl = "http://api.supplier.shopmell.com"
        self.sheetName = sheet

    def return_id(self):
        """根据每个模块的list 或者 page接口查找id"""
        id_list = []
        sheets = self.workBook.sheet_names()
        for sheet in sheets:
            if sheet == self.sheetName:
                work_sheet = self.workBook.sheet_by_name(sheet)
                for row in range(work_sheet.nrows):
                    row_value = work_sheet.row_values(row)
                    if row_value[3][-5:] == "/page":
                        api_message = [row_value[0], row_value[2], row_value[3], row_value[4], row_value[5], row_value[6]]
                        if api_message:
                            data = CommonApi().request_to_send(
                                method=api_message[3], url=api_message[2], body=api_message[5].replace("'", '"'), header=header)
                            print(data.json()['data'])
                            for result in data.json()['data']['data']:
                                if "id" in result:
                                    id_list.append(result['id'])
                #  page未获取到ID 使用list获取ID
                if not id_list:
                    for row in range(work_sheet.nrows):
                        row_value = work_sheet.row_values(row)
                        if row_value[3][-5:] == "/list":
                            api_message = [row_value[0], row_value[2], row_value[3], row_value[4], row_value[5], row_value[6]]
                            if api_message:
                                data = CommonApi().request_to_send(
                                    method=api_message[3], url=api_message[2], body=api_message[5].replace("'", '"'), header=header)
                                for result in data.json()['data']:
                                    if "id" in result:
                                        id_list.append(result['id'])
        if id_list:
            return max(id_list)
        elif not id_list:
            return None

    def return_api_message(self):
        """返回接口所需要的信息"""
        api_message = []
        sheets = self.workBook.sheet_names()
        for sheet in sheets:
            # if "运费账单管理" in sheet or "文件管理" in sheet or "ueditor" in sheet or "素材分组模版" in sheet or "电商平台承运商" in sheet\
            #         or "电商平台" in sheet or "商品订单管理" in sheet or "角色权限关系" in sheet or "建站模板管理" in sheet or "标签关系(admin共用)" in sheet\
            #         or "交易明细管理" in sheet or "初始化" in sheet:  # admin需要特殊处理的数据，先剔除
            #     pass
            if "文件上传" in sheet:
                pass
            else:
                if sheet == self.sheetName:  # 调试
                    work_sheet = self.workBook.sheet_by_name(sheet)

                    for row in range(work_sheet.nrows):
                        row_value = work_sheet.row_values(row)
                        if "add" in row_value[3] or "edit" in row_value[3] or "read" in row_value[3]:
                            api_message.append((row_value[0], row_value[2], row_value[3], row_value[4], row_value[6]))

                    for row in range(work_sheet.nrows):
                        row_value = work_sheet.row_values(row)
                        if row_value[0] == "模块" or "edit" in row_value[2] or "add" in row_value[2]\
                                or row_value[6] == "File" or "delete" in row_value[3] or "read" in row_value[3]:
                            pass
                        else:
                            api_message.append((row_value[0], row_value[2], row_value[3], row_value[4], row_value[6]))

                    for row in range(work_sheet.nrows):
                        row_value = work_sheet.row_values(row)
                        if "delete" in row_value[3]:
                            api_message.append((row_value[0], row_value[2], row_value[3], row_value[4], row_value[6]))

        return api_message


if __name__ == '__main__':
    api = GainApiData(file_name="erp-api.xls", sheet="争议管理")
    print(api.return_id())
    # for me in api.return_api_message():
    #     if me[4] == "File":
    #         pass
    #     else:
    #         da = CommonApi().request_to_send(
    #             method=me[3], url=me[2], body=me[4].replace("'", '"'), header=header, param_id=api.return_id()
    #         )
    #         print(f"{me[1]}{da.json()}")
    #         if "message" in da.json():
    #             if da.json()['message'] == 'success':
    #                 print("----成功----")
    #             else:
    #                 print("----失败----")
    #         else:
    #             print("没有message")
    # for m in api.return_api_message():
    #     if m[4] == "File":
    #         pass
    #     else:
    #         print(m)
