#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: base_result.py
# 说   明: 
# 创建时间: 2021/11/2 23:26
# @Version：V 0.1
# @desc : 自定义接口返回结果


class BaseResult:

    def __init__(self):
        self.success = False
        self.status_code = 200
        self.error = ""
        self.response = ""
        self.message = ""
        self.code = 0
        self.text = {}

    def default_assert(self, response):
        """
        默认断言
        :param response:
        :return:
        """
        self.response = response
        self.status_code = response.status_code
        if response.status_code == 200:
            self.success = True
        else:
            self.error = "接口返回码是 {}，返回信息：{}".format(self.status_code, response.text)
        try:
            self.text = self.response.json()
        except Exception as error:
            self.text = self.response.content
        return self
