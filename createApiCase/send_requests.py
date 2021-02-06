#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Author: 王小飞
@File  : send_requests.py
@Time  : 2021/1/15 10:06
@Tool  : PyCharm
"""
import requests
import urllib3
import json


class RequestsTest(object):

    def __init__(self):
        self.warnings = urllib3.disable_warnings()
        self.session = requests.Session()

    def send_requests(self, method, url, param_type, body=None, **kwargs):
        """发送请求"""
        method = method.upper()
        param_type = param_type.upper()
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except BaseException as err:
                body = eval(body)
                print(err)
        if method == "POST":
            if param_type == "JSON":
                response = self.session.request(
                    method=method, url=url, json=body, verify=False, **kwargs)
            elif param_type == "FROM":
                response = self.session.request(
                    method=method, url=url, data=body, verify=False, **kwargs)
            elif param_type == "MULTIPART":
                response = self.session.request(
                    method=method, url=url, files=body, verify=False, **kwargs)
            else:
                raise TypeError(f"{method}-未定义的参数类型！")
            return response
        elif method == "GET":
            response = self.session.request(
                method=method, url=url, params=body, verify=False, **kwargs)
            return response
        else:
            raise TypeError(f"{method}-请求方法未定义！")

    def __call__(self, method, url, param_type, body=None, **kwargs):
        return self.send_requests(
            method=method, url=url, param_type=param_type, body=body, **kwargs)

    def close_session(self):
        """结束会话"""
        self.session.close()
        del self.session.cookies


request = RequestsTest()


if __name__ == '__main__':
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                            " (KHTML, like Gecko)Chrome/84.0.4147.105 Safari/537.36",
              "Content-Type": "application/json"}

    a = request(method="POST", url="http://api.admin.shopmell.com/admin/passport/login", param_type="JSON",
                body="""{"account": "admin", "password": "HUIQMGMM"}""", headers=header).json()
    print(a)
    request.close_session()
