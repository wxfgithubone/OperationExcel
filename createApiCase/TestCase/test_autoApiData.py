#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Author: 王小飞
@File  : test_autoApiData.py
@Time  : 2021/1/15 15:12
@Tool  : PyCharm
"""
import pytest
import allure
import sys
sys.path.append(r'E:\Desktop\ParsSwagger\createApiCase\TestCase')
from commonApi import CommonApi
from gainApiDta import GainApiData, header


api = GainApiData(file_name="erp-api.xls", sheet="01.公共模块")


@allure.epic("admin接口自动化项目")
class TestCommonApi:

    @pytest.mark.parametrize("model_name, api_name, path, method, payload", api.return_api_message())
    def test_case_one(self, model_name, api_name, path, method, payload):
        if payload == "File":
            pass
        else:
            resp = CommonApi().request_to_send(
                method=method, url=path, body=payload.replace("'", '"'), header=header, param_id=api.return_id()
            )
            if "message" in resp.json():
                print(resp.json())
                assert resp.json()['message'] == 'success'
            else:
                assert resp.status_code == 200
            allure.dynamic.story(model_name), allure.dynamic.title(api_name)
            allure.dynamic.description("代码生成，暂无描述！"), allure.dynamic.severity("blocker")


if __name__ == '__main__':
    pytest.main(['-v', '-s'])
