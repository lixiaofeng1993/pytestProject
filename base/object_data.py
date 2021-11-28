#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: object_data.py
# 说   明: 
# 创建时间: 2021/11/20 12:34
# @Version：V 0.1
# @desc : 封装测试数据为对象

from public.case_step import *


def object_data(test_data: dict, file_path: str):
    """
    封装测试数据为对象
    :param test_data: 测试数据
    :param file_path: 测试数据文件路径
    :return: 字典包含的数据对象
    """
    _data = dict()
    flag = False
    case_step_key = ["case_step_1", "case_step_2", "case_step_3", "case_step_4", "case_step_5"]
    for keys, values in test_data.items():
        _data[keys] = {}
        if isinstance(values, dict):
            for ori_key in values.keys():
                if ori_key not in case_step_key:
                    flag = True
                if values.get("path") and values.get("method"):
                    flag = False  # 参数化存在依赖的情况，只能走这里
            if not flag:
                _data[keys] = ObjectData()
                if values.get("path") and values.get("method"):
                    case_step(_data[keys], values, file_path)
                for key, value in values.items():
                    if isinstance(value, dict):
                        if value.get("path") and value.get("method"):
                            if key == "case_step_1":
                                case_step_1(_data[keys], value, file_path)
                            elif key == "case_step_2":
                                case_step_2(_data[keys], value, file_path)
                            elif key == "case_step_3":
                                case_step_3(_data[keys], value, file_path)
                            elif key == "case_step_4":
                                case_step_4(_data[keys], value, file_path)
                            elif key == "case_step_5":
                                case_step_5(_data[keys], value, file_path)
            else:
                for key, value in values.items():
                    if isinstance(value, dict):
                        if value.get("path") and value.get("method"):
                            _data[keys][key] = ObjectData()
                            case_step(_data[keys][key], value, file_path)
    _data.update({
        "epic": test_data.get("epic"),
        "feature": test_data.get("feature")
    })
    return _data
