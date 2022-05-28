#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: bae_request.py
# 说   明: 
# 创建时间: 2021/11/2 18:54
# @Version：V 0.1
# @desc : requests 请求方式封装
import requests
import urllib3
from urllib import parse
import json as alias_json
from public.log import logger
from public import exceptions
from base.base_result import BaseResult


class BaseRequest:

    def __init__(self):
        self.session = requests.session()

    def request(self, url: str, method: str, headers: dict, params: dict, data: str, json: dict,
                files=None) -> BaseResult:
        """
        requests 请求封装
        :param url: 完整的url地址
        :param method: 请求方式
        :param headers: 请求头
        :param params: get请求传参
        :param data: 请求体
        :param json: 请求体
        :param files: 上传文件对象
        :return: 自定义 BaseResult 对象
        """
        params = parse.urlencode(params, quote_via=parse.quote) if params else {}  # get请求参数 urlencode 转码
        if files:
            data = files
        logger.info("接口请求地址 ==>> {}".format(url))
        logger.info("接口请求方式 ==>> {}".format(method))
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        logger.info("接口请求头 ==>> {}".format(alias_json.dumps(headers, indent=4, ensure_ascii=False)))
        logger.info("接口请求 params 参数 ==>> {}".format(alias_json.dumps(params, indent=4, ensure_ascii=False)))
        logger.info(f"接口请求体 data 参数 ==>> {data}")
        logger.info("接口请求体 json 参数 ==>> {}".format(alias_json.dumps(json, indent=4, ensure_ascii=False)))
        logger.info("接口上传附件 files 参数 ==>> {}".format(files))

        urllib3.disable_warnings()  # 忽略警告
        try:
            response = self.session.request(url=url, method=method, headers=headers, params=params, data=data,
                                            json=json, verify=False)
            result = BaseResult().default_assert(response)
            # result = BaseResult().default_assert(Response())
            logger.info(f"接口返回信息 ==>> {str(result.text)[:500]}")
        except requests.exceptions.Timeout as error:
            raise requests.exceptions.Timeout(f"接口请求超时错误 ==>> {url} -> {error}")
        except Exception as error:
            raise exceptions.InterfaceRequestError(f"接口请求出现异常 ==>> {error}")
        return result


class Response:
    def __init__(self):
        self.success = False
        self.status_code = 200
        self.error = ""
        self.response = ""
        self.message = ""
        self.code = 0
        self.text = {}

    def json(self):
        return {
            "code": self.code,
            "message": "请求成功",
        }
