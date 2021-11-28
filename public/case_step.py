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
        self.body = {}
        self.extract = {}
        self.validate = {}
        self.story = ""
        self.title = ""
        self.step = ""
        self.description = ""
        self.file_path = ""
        self.upload = {}
        self.case_step_1 = CaseStep()
        self.case_step_2 = CaseStep()
        self.case_step_3 = CaseStep()
        self.case_step_4 = CaseStep()
        self.case_step_5 = CaseStep()


class CaseStep:

    def __init__(self):
        self.path = ""
        self.method = ""
        self.headers = {}
        self.parametrize = []
        self.params = {}
        self.body = {}
        self.extract = {}
        self.validate = {}
        self.story = ""
        self.title = ""
        self.step = ""
        self.description = ""
        self.file_path = ""
        self.upload = {}


def case_step(data_obj, value, file_path):
    data_obj.path = value.get("path")
    data_obj.method = value.get("method")
    data_obj.headers = value.get("headers")
    data_obj.parametrize = value.get("parametrize")
    data_obj.params = value.get("params")
    data_obj.body = value.get("body")
    data_obj.extract = value.get("extract")
    data_obj.validate = value.get("validate")
    data_obj.story = value.get("story")
    data_obj.title = value.get("title")
    data_obj.step = value.get("step")
    data_obj.description = value.get("description")
    data_obj.file_path = file_path
    data_obj.upload = value.get("upload")
    return data_obj


def case_step_1(data_obj, value, file_path):
    data_obj.case_step_1.path = value.get("path")
    data_obj.case_step_1.method = value.get("method")
    data_obj.case_step_1.headers = value.get("headers")
    data_obj.case_step_1.parametrize = value.get("parametrize")
    data_obj.case_step_1.params = value.get("params")
    data_obj.case_step_1.body = value.get("body")
    data_obj.case_step_1.extract = value.get("extract")
    data_obj.case_step_1.validate = value.get("validate")
    data_obj.case_step_1.story = value.get("story")
    data_obj.case_step_1.title = value.get("title")
    data_obj.case_step_1.step = value.get("step")
    data_obj.case_step_1.description = value.get("description")
    data_obj.case_step_1.file_path = file_path
    data_obj.case_step_1.upload = value.get("upload")
    return data_obj


def case_step_2(data_obj, value, file_path):
    data_obj.case_step_2.path = value.get("path")
    data_obj.case_step_2.method = value.get("method")
    data_obj.case_step_2.headers = value.get("headers")
    data_obj.case_step_2.parametrize = value.get("parametrize")
    data_obj.case_step_2.params = value.get("params")
    data_obj.case_step_2.body = value.get("body")
    data_obj.case_step_2.extract = value.get("extract")
    data_obj.case_step_2.validate = value.get("validate")
    data_obj.case_step_2.story = value.get("story")
    data_obj.case_step_2.title = value.get("title")
    data_obj.case_step_2.step = value.get("step")
    data_obj.case_step_2.description = value.get("description")
    data_obj.case_step_2.file_path = file_path
    data_obj.case_step_2.upload = value.get("upload")
    return data_obj


def case_step_3(data_obj, value, file_path):
    data_obj.case_step_3.path = value.get("path")
    data_obj.case_step_3.method = value.get("method")
    data_obj.case_step_3.headers = value.get("headers")
    data_obj.case_step_3.parametrize = value.get("parametrize")
    data_obj.case_step_3.params = value.get("params")
    data_obj.case_step_3.body = value.get("body")
    data_obj.case_step_3.extract = value.get("extract")
    data_obj.case_step_3.validate = value.get("validate")
    data_obj.case_step_3.story = value.get("story")
    data_obj.case_step_3.title = value.get("title")
    data_obj.case_step_3.step = value.get("step")
    data_obj.case_step_3.description = value.get("description")
    data_obj.case_step_3.file_path = file_path
    data_obj.case_step_3.upload = value.get("upload")
    return data_obj


def case_step_4(data_obj, value, file_path):
    data_obj.case_step_4.path = value.get("path")
    data_obj.case_step_4.method = value.get("method")
    data_obj.case_step_4.headers = value.get("headers")
    data_obj.case_step_4.parametrize = value.get("parametrize")
    data_obj.case_step_4.params = value.get("params")
    data_obj.case_step_4.body = value.get("body")
    data_obj.case_step_4.extract = value.get("extract")
    data_obj.case_step_4.validate = value.get("validate")
    data_obj.case_step_4.story = value.get("story")
    data_obj.case_step_4.title = value.get("title")
    data_obj.case_step_4.step = value.get("step")
    data_obj.case_step_4.description = value.get("description")
    data_obj.case_step_4.file_path = file_path
    data_obj.case_step_4.upload = value.get("upload")
    return data_obj


def case_step_5(data_obj, value, file_path):
    data_obj.case_step_5.path = value.get("path")
    data_obj.case_step_5.method = value.get("method")
    data_obj.case_step_5.headers = value.get("headers")
    data_obj.case_step_5.parametrize = value.get("parametrize")
    data_obj.case_step_5.params = value.get("params")
    data_obj.case_step_5.body = value.get("body")
    data_obj.case_step_5.extract = value.get("extract")
    data_obj.case_step_5.validate = value.get("validate")
    data_obj.case_step_5.story = value.get("story")
    data_obj.case_step_5.title = value.get("title")
    data_obj.case_step_5.step = value.get("step")
    data_obj.case_step_5.description = value.get("description")
    data_obj.case_step_5.file_path = file_path
    data_obj.case_step_5.upload = value.get("upload")
    return data_obj
