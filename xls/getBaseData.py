#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Author: 王小飞
@File  : getBaseData.py
@Time  : 2021/1/7 10:20
@Tool  : PyCharm
"""
import requests
import json
import yaml
from multiprocessing import Process
from excel import SwaggerData, remove_empty_lines, file_compare


def _wrap_colour(colour, *args):
    for message in args:
        print(colour + '{}'.format(message) + '\033[0m')


# 控制台彩色打印
def blue(*args): _wrap_colour('\033[94m', *args)  # 蓝色
def bold(*args): _wrap_colour('\033[1m', *args)  # 粗体
def cyan(*args): _wrap_colour('\033[96m', *args)  # 青绿色
def green(*args): _wrap_colour('\033[92m', *args)  # 绿色
def pink(*args): _wrap_colour('\033[95m', *args)  # 粉红色
def purple(*args): _wrap_colour('\033[035m', *args)  # 紫色
def red(*args): _wrap_colour('\033[91m', *args)  # 红色
def underline(*args): _wrap_colour('\033[4m', *args)  # 下划线
def yellow(*args): _wrap_colour('\033[93m', *args)  # 黄色


post, get, put, delete, patch, options, head, unknown, total = 0, 0, 0, 0, 0, 0, 0, 0, 0  # （全局变量）统计请求方式


def read_swagger(url_key):
    """读取swagger文档，按接口属性拆分"""
    with open("./config.yml", "r", encoding="utf-8") as config_file:
        _config = yaml.load(config_file.read(), yaml.FullLoader)  # 配置文件
    # 统计接口比例
    intact_api_number, nest_api_number, only_body, only_header, no_body_and_header = 0, 0, 0, 0, 0
    schema_not_definitions, no_schema = 0, 0
    all_data_list, qt_list = [], []
    url_dict = _config['url']
    green(f"获取{url_key}-Swagger文档数据...")
    with open(f"api/{url_key}-api.txt", "w+", encoding="utf-8") as fi:
        fi.write(requests.post(url=f"{url_dict[url_key]}/v2/api-docs", headers=_config['header']).text)

    def count(meth):
        """统计请求方法"""
        global post, get, put, delete, patch, options, head, unknown
        if meth.upper() == "POST":
            post += 1
        elif meth.upper() == "GET":
            get += 1
        elif meth.upper() == "PUT":
            put += 1
        elif meth.upper() == "DELETE":
            delete += 1
        elif meth.upper() == "PATCH":
            patch += 1
        elif meth.upper() == "OPTIONS":
            options += 1
        elif meth.upper() == "HEAD":
            head += 1
        else:
            unknown += 1

    def return_type(types):
        """返回参数类型"""
        if types == "string":
            body = 'string'
        elif types == "integer":
            body = int(0)
        elif types == "array":
            body = []
        elif types == "file":
            body = "File"
        else:
            body = "unknown"
        return body

    green(f"正在读取{url_key}里的数据...")
    with open(f"api/{url_key}-api.txt", "r+", encoding="utf-8") as f:
        global total, post, get, put, delete, patch, options, head, unknown  # 声明全局变量
        dc_data = json.loads(f.read())  # json转字典
        for request_path, value in dc_data['paths'].items():
            for method, msg in value.items():
                module_name, api_name = msg['tags'][0], msg['summary']  # 接口模块名称、接口名称
                api_id, api_repose = msg['operationId'], msg['responses']  # 接口id、接口响应示例
                if 'description' in msg:
                    api_description = msg['description']  # 接口描述
                else:
                    api_description = "No description"
                if "consumes" in msg and "parameters" in msg:  # 请求头和请参数都有
                    header = msg['consumes'][0]  # 请求头
                    if "schema" in msg['parameters'][0]:
                        if "originalRef" in msg['parameters'][0]['schema']:

                            # 遍历带有参数的字典
                            for i, j in dc_data['definitions'].items():
                                if msg['parameters'][0]['schema']['originalRef'] == j['title']:
                                    intact_api_number += 1  # 统计带有请求参数的接口
                                    payload = {}  # 请求参数
                                    for body_header, body_explain in j['properties'].items():

                                        # 嵌套的json
                                        if "items" in body_explain and 'originalRef' in body_explain['items']:
                                            nest_api_number += 1
                                            if body_explain['type'] == "array" and "items" in body_explain:  # 嵌套json的类型为list
                                                qt_list.append((request_path, api_name))  # 嵌套json的接口地址
                                                payload2, nest_list1 = {}, []
                                                payload[body_header] = nest_list1
                                                for i2, j2 in dc_data['definitions'].items():
                                                    if body_explain['items']['originalRef'] == j2['title']:
                                                        for body_header2, body_explain2 in j2['properties'].items():
                                                            # 多层嵌套的json
                                                            payload2_1, nest_list1_1 = {}, []
                                                            if "type" in body_explain2:
                                                                if body_explain2['type'] == "array" and "items" in body_explain2:
                                                                    for i2_1, j2_1 in dc_data['definitions'].items():
                                                                        if body_explain2['items']['originalRef'] == j2_1['title']:
                                                                            for body_header2_1, body_explain2_1 in j2_1['properties'].items():
                                                                                # 如果再有更深的嵌套，在下面加 if...for...else...
                                                                                payload2_1[body_header2_1] = return_type(types=body_explain2_1['type'])
                                                                    nest_list1_1.append(payload2_1)
                                                                    payload2[body_header2] = nest_list1_1
                                                                else:
                                                                    payload2[body_header2] = return_type(types=body_explain2['type'])
                                                            # 没有type字段的
                                                            else:
                                                                if "originalRef" in body_explain2:
                                                                    for i2_2, j2_2 in dc_data['definitions'].items():
                                                                        if body_explain2['originalRef'] == j2_2['title']:
                                                                            for body_header2_2, body_explain2_2 in j2_2['properties'].items():
                                                                                payload2_1[body_header2_2] = return_type(types=body_explain2_2['type'])
                                                                payload2[body_header2] = payload2_1  # 将嵌套的json合并到一起
                                                nest_list1.append(payload2)  # list储存嵌套字典
                                            else:
                                                raise ValueError("这里有非list嵌套的json数据未做处理！！！", request_path)
                                        # 单个嵌套的json
                                        elif "originalRef" in body_explain:
                                            payload3 = {}
                                            payload[body_header] = payload3
                                            for i3, j3 in dc_data['definitions'].items():
                                                if body_explain['originalRef'] == j3['title']:
                                                    for body_header3, body_explain3 in j3['properties'].items():
                                                        payload3[body_header3] = return_type(types=body_explain3['type'])
                                        # 非嵌套json
                                        else:
                                            if "type" in body_explain:
                                                payload[body_header] = return_type(types=body_explain['type'])
                                            else:
                                                payload[body_header] = "None"
                                                raise ValueError("这里有未知的参数类型！！！\n", request_path, body_explain)

                                    all_data_list.append(
                                        [module_name, api_id, api_name, request_path, method.upper(),
                                         header, payload, j['properties'], api_description, api_repose, "$.message"]
                                    )
                                    # blue("完整属性的接口\n模块:{}\n接口名称：{}\n接口ID：{}\n请求路径：{}\n请求方法：{}\n请求头：{}\n请求体：{}\n参数说明：{}\n".
                                    #      format(module_name, api_id, api_name, request_path, method.upper(), header, payload, j['properties']))
                                    count(meth=method)
                                    total += 1

                        else:
                            schema_not_definitions += 1
                            total += 1
                            count(meth=method)

                            if msg['parameters'][0]['schema']:  # 参数为[]
                                if msg['parameters'][0]['schema']['type'] == "array":
                                    da_1 = return_type(types=msg['parameters'][0]['schema']['type'])
                                    da_1.append(int(0))
                                else:
                                    da_1 = return_type(types=msg['parameters'][0]['schema']['type'])
                            else:
                                raise ("未知的数据类型！！！", request_path)

                            all_data_list.append(
                                [module_name, api_id, api_name, request_path, method.upper(), header,
                                 da_1, msg['parameters'], api_description, api_repose, "$.message"]
                            )
                            # cyan(f"参数概要（schema）不在（definitions）里\n模块:{module_name}\n接口ID：{api_id}\n"
                            #      f"接口名称：{api_name}\n请求路径：{request_path}\n请求方法：{method.upper()}\n请求头：{header}"
                            #      f"\n请求体：{da_1}\n详细信息：{msg['parameters']}\n")
                    else:
                        no_schema += 1
                        total += 1
                        count(meth=method)
                        post_data_list = []
                        for key in msg['parameters']:
                            if "type" in key:
                                post_data_list.append(f"{key['name']}={return_type(types=key['type'])}")
                        post_data_list2 = "&".join(post_data_list)
                        if "{" in request_path:
                            x, y = request_path.index("{"), request_path.index("}")
                            place = request_path[x:y+1]
                            re_pa = request_path.replace(place, "{params}")

                            all_data_list.append(
                                [module_name, api_id, api_name, re_pa, method.upper(), header,
                                 "{参数在请求路径里}", msg['parameters'], api_description, api_repose, "$.message"]
                            )
                            # pink(f"没有参数概要（schema）\n模块:{module_name}\n接口ID：{api_id}\n接口名称：{api_name}\n请求路径：{re_pa}\n"
                            #      f"请求方法：{method.upper()}\n求请头：{header}\n请求体：No\n详细信息{msg['parameters']}\n")

                        elif msg['parameters'][0]['type'] == "file":
                            all_data_list.append(
                                [module_name, api_id, api_name, request_path, method.upper(), header,
                                 "File", msg['parameters'], api_description, api_repose, "$.message"]
                            )
                            # pink(f"没有参数概要（schema）\n模块:{module_name}\n接口ID：{api_id}\n接口名称：{api_name}\n请求路径：{request_path}\n"
                            #      f"请求方法：{method.upper()}\n请求头：{header}\n请求体：File\n详细信息{msg['parameters']}\n")

                        elif msg['parameters'][0]['in'] == "query":
                            all_data_list.append(
                                [module_name, api_id, api_name, request_path, method.upper(), header,
                                 post_data_list2, msg['parameters'], api_description, api_repose, "$.message"]
                            )
                            # pink(f"没有参数概要（schema）\n模块:{module_name}\n接口ID：{api_id}\n接口名称：{api_name}\n请求路径：{request_path}\n"
                            #      f"请求方法：{method.upper()}\n请求头：{header}\n请求体：{post_data_list2}\n详细信息{msg['parameters']}\n")

                        else:
                            all_data_list.append(
                                [module_name, api_id, api_name, request_path, method.upper(), header,
                                 "未知！", msg['parameters'], api_description, api_repose, "$.message"]
                            )
                            raise ValueError(f"没有参数概要（schema）\n模块:{module_name}\n接口ID：{api_id}\n"
                                             f"接口名称：{api_name}\n请求路径：{request_path}\n请求方法：{method.upper()}"
                                             f"\n请求头：{header}\n请求体：未知！\n详细信息{msg['parameters']}\n")

                elif "parameters" in msg:  # 没有请求头只有参数
                    only_header += 1
                    total += 1
                    count(meth=method)
                    get_data_list = []
                    for key in msg['parameters']:
                        get_data_list.append(f"{key['name']}={return_type(types=key['type'])}")
                    get_data_list2 = "&".join(get_data_list)  # 拼接成get请求路径
                    if msg['parameters'][0]['in'] == "query":

                        all_data_list.append(
                            [module_name, api_id, api_name, f"{request_path}?{get_data_list2}", method.upper(),
                             "No", f"?{get_data_list2}", msg, api_description, api_repose, "$.message"]
                        )
                        # green(f"没有请求头但是有参数\n模块:{module_name}\n接口ID：{api_id}\n接口名称{api_name}"
                        #       f"\n请求路径：{request_path}?{get_data_list2}"
                        #       f"\n请求方法:{method.upper()}\n请求头：No\n请求体：?{get_data_list2}\n详细信息：{msg}\n")

                    elif "{" in request_path:
                        x, y = request_path.index("{"), request_path.index("}")
                        place = request_path[x:y + 1]
                        re_pa = request_path.replace(place, "{params}")

                        all_data_list.append(
                            [module_name, api_id, api_name, re_pa, method.upper(), "No", "{参数在请求路径里}",
                             msg, api_description, api_repose, "$.message"]
                        )
                        # green(f"ID为0没有请求头但是有参数\n模块:{module_name}\n接口ID：{api_id}\n接口名称{api_name}\n"
                        #       f"请求路径：{re_pa}\n请求方法:{method.upper()}\n请求头：No\n请求体：No\n详细信息：{msg}\n")

                    else:
                        all_data_list.append(
                            [module_name, api_id, api_name, request_path, method.upper(), "No", "No",
                             msg, api_description, api_repose, "$.message"]
                        )
                        # green(f"没有请求头但是有参数\n模块:{module_name}\n接口ID：{api_id}\n接口名称{api_name}\n"
                        #       f"请求路径：{request_path}\n请求方法:{method.upper()}\n请求头：No\n请求体：No\n详细信息：{msg}\n")

                elif "consumes" in msg:  # 只有请求头没有参数
                    only_body += 1
                    total += 1
                    count(meth=method)

                    all_data_list.append(
                        [module_name, api_id, api_name, request_path, method.upper(),
                         msg['consumes'][0], "No", msg, api_description, api_repose, "$.message"]
                    )
                    # bold(f"无需传参的：\n模块:{module_name}\n接口ID：{api_id}\n接口名称{api_name}\n请求路径：{request_path}\n"
                    #      f"请求方法：{method.upper()}\n请求头：{msg['consumes'][0]}\n请求参数：No\n详细信息：{msg}\n")

                elif "consumes" not in msg and "parameters" not in msg:  # 请求头，请求参数都没有
                    no_body_and_header += 1
                    total += 1
                    count(meth=method)

                    all_data_list.append(
                        [module_name, api_id, api_name, request_path, method.upper(),
                         "No", "No", msg, api_description, api_repose, "$.message"]
                    )
                    # yellow(f"参数和请求头都不需要\n模块:{module_name}\n接口ID：{api_id}\n接口名称{api_name}\n请求路径：{request_path}\n"
                    #        f"请求方法：{method.upper()}\n请求头：No\n请求参数：No\n详细信息：{msg}\n")
                else:
                    raise ValueError(f"未知的内容！{request_path}{msg}")

        # 打印接口概要信息
        print("{}接口文档一共{}个接口，完整属性接口总数{}个(其中嵌套json{}个)，只有请求头的接口{}个，只有参数的接口{}个，无头无参数的接口{}个\n"
              "参数概要（schema）不在（definitions）里 {} 个，没有参数概要（schema）{} 个\n"
              "POST：{}个，GET：{}个，PUT：{}个，DELETE：{}个，PATCH：{}个，OPTIONS：{}个，HEAD：{}个，未知的：{}个".
              format(url_key, total, intact_api_number, nest_api_number, only_header, only_body, no_body_and_header,
                     schema_not_definitions, no_schema, post, get, put, delete, patch, options, head, unknown))

        sheets = []  # 所有的表单名称
        for k in [sh[0] for sh in all_data_list]:
            if k not in sheets:
                sheets.append(k)

        # 定义excel标题行
        first_col_data = [
            "模块", "接口ID", "接口名称", "路径", "请求方法", "请求头",
            "请求体", "请求参数描述", "接口描述", "响应信息描述", "检查点", "实际结果"
        ]

        # 写入excel
        green(f"正在将{url_key}数据写入excel...")
        SwaggerData(
            file_path=f"./init_data/{url_key}.xls", sheets=sheets,
            first_col_data=first_col_data, all_data=all_data_list
        )

        # 去除excel中的空行
        try:
            print("正在去除空格，重新生成excel...")
            remove_empty_lines(
                first_col_data=first_col_data,
                initial_file_path=f"./init_data/{url_key}.xls",
                new_file_path=f"./new_data/{url_key}-api.xls"
            )
        except BaseException:
            raise
        else:
            green("success!")
        finally:
            print(f"{url_key}项目读取结束！")

        # 对比是否有新增接口
        blue(f"开始对比{url_key}-api用例...")
        try:
            file_compare(
                new_file_path=f"./new_data/{url_key}-api.xls",
                old_file_path=f"./old_data/{url_key}-api.xls",
                copy_file_path=f"./old_data/{url_key}-api.xls"
            )
        except BaseException as err:
            raise err
        else:
            green(f"{url_key}-api.xls用例更新完成！")


if __name__ == '__main__':
    threads = [
        Process(target=read_swagger, args=("admin",)), Process(target=read_swagger, args=("supplier",)),
        Process(target=read_swagger, args=("erp",))
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # read_swagger(url_key="call")
