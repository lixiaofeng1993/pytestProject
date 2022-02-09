#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: case_step.py
# 说   明: 
# 创建时间: 2021/11/21 18:26
# @Version：V 0.1
# @desc : 测试数据对象化处理

class ObjectData:

    def __init__(self):
        self.path = ""
        self.method = ""
        self.headers = {}
        self.parametrize = []
        self.params = {}
        self.data = {}
        self.json = {}
        self.extract = {}
        self.validate = {}
        self.story = ""
        self.title = ""
        self.step = ""
        self.description = ""
        self.file_path = ""
        self.upload = {}
        self.variable = {}


class CaseStep:

    def __init__(self):
        self.path = ""
        self.method = ""
        self.headers = {}
        self.parametrize = []
        self.params = {}
        self.data = {}
        self.json = {}
        self.extract = {}
        self.validate = {}
        self.story = ""
        self.title = ""
        self.step = ""
        self.description = ""
        self.file_path = ""
        self.upload = {}
        self.variable = {}
