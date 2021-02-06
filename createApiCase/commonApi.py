#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Author: 王小飞
@File  : commonApi.py
@Time  : 2021/1/15 11:07
@Tool  : PyCharm
"""
import requests

he = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    " (KHTML, like Gecko)Chrome/84.0.4147.105 Safari/537.36",
      "Content-Type": "application/json"}


class CommonApi:
    """项目公共的接口请求类"""
    def __init__(self):
        self.session = requests.Session()
        self.baseUrl = "http://api.erp.shopmell.com"
        base_url = f"{self.baseUrl}/erp/dealer/passport/login"
        body = {'account': 'lionamz', 'password': 'ljx@2019'}
        resp = self.session.post(url=base_url, json=body, headers=he)
        self.cookie = {"LJXD_COOKIE_SESSION_NAME": resp.cookies['LJXD_COOKIE_SESSION_NAME']}
        self.login = lambda: self.session.post(url=base_url, json=body, headers=he)

    def request_to_send(self, method, url, body=None, header=None, param_id=None):
        """发送HTTP请求，POST、GET"""
        if method == "POST":
            if "edit" in url:
                body = eval(body)
                if "id" in body:
                    body['id'] = param_id
                    response = self.session.post(url=f"{self.baseUrl}{url}", json=body, headers=header, verify=False)
                else:
                    raise ValueError(f"{url}-未找到关键字ID")
            elif body == "No" or "请求路径" in body:
                response = self.session.post(url=f"{self.baseUrl}{url}", headers=header, verify=False)
            elif "请求路径" in body:
                response = self.session.post(url=f"{self.baseUrl}{url}{param_id}")
            elif body == "[0]":
                response = self.session.post(url=f"{self.baseUrl}{url}", json=[param_id], headers=header, verify=False)
            elif body == "{ID}":
                response = self.session.post(url=f"{self.baseUrl}{url}{param_id}", headers=header, verify=False)
            elif "=" in body:
                response = self.session.post(url=f"{self.baseUrl}{url}", data=body, headers=header, verify=False)
            else:
                body = eval(body)
                response = self.session.post(url=f"{self.baseUrl}{url}", json=body, headers=header, verify=False)
            return response

        elif method == "GET":
            if body == "No" or "请求路径" in body or "?" in body:
                response = self.session.get(url=f"{self.baseUrl}{url}", headers=header, verify=False)
            elif body == "{ID}":
                response = self.session.get(url=f"{self.baseUrl}{url}{param_id}", headers=header, verify=False)
            else:
                body = eval(body)
                response = self.session.get(url=f"{self.baseUrl}{url}", params=body, headers=header, verify=False)
            return response

        else:
            raise TypeError(f"{method}该请求方法未定义！")


if __name__ == '__main__':

    api = CommonApi()

    print(api.request_to_send(
        method="GET", url="/erp/dealer/passport/toLogin", body="""No""", header=he
    ).json())
    print(api.login().json())



