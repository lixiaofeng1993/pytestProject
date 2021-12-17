#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: object_data.py
# 说   明: 
# 创建时间: 2021/11/20 12:34
# @Version：V 0.1
# @desc : 封装测试数据为对象

from public.case_step import *


def object_data(test_data: dict, file_path: str, case_step_num=10):
    """
    封装测试数据为对象
    :param test_data: 测试数据
    :param file_path: 测试数据文件路径
    :param case_step_num: 测试用例依赖接口数量
    :return: 字典包含的数据对象
    """
    obj = dict()
    case_step_list = list()
    case_step_num = int(case_step_num) if str(case_step_num).isdigit() else 10
    case_step_num = 10 if case_step_num < 10 else case_step_num
    for i in range(1, case_step_num + 1):
        case_step_list.append(f"case_step_{i}")
    for keys, values in test_data.items():
        obj[keys] = ObjectData()
        if isinstance(values, dict):
            for key, value in values.items():
                setattr(obj[keys], key, value)
                setattr(obj[keys], "file_path", file_path)
                if isinstance(value, dict):
                    step = CaseStep()
                    for k, v in value.items():
                        setattr(step, k, v)
                        setattr(step, "file_path", file_path)
                    if key in case_step_list:
                        setattr(obj[keys], key, step)
    obj.update({
        "epic": test_data.get("epic"),
        "feature": test_data.get("feature")
    })
    return obj
