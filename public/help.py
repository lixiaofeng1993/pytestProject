#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: help.py
# 说   明: 
# 创建时间: 2021/11/2 18:54
# @Version：V 0.1
# @desc : 项目常用路径

import os
import io
import platform
import time
import inspect
import allure
from public import exceptions

# 项目根目录
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
patt = "\\" if platform.system() == "Windows" else "/"


def report_setting(data):
    """
    allure 报告目录
    """
    title = data.title
    if data.parametrize:
        for params in data.parametrize:
            if isinstance(params, dict):
                if params.get("case_name"):
                    title = params["case_name"]
    allure.dynamic.story(data.story)
    allure.dynamic.title(title)
    allure.dynamic.description(data.description)


def report_step_setting(data):
    """
    allure 步骤
    """
    with allure.step(data.step):
        pass


def check(path):
    """
    检查文件是否存在，不存在则抛 FileNotFoundError
    :param path:
    :return:
    """
    if not os.path.exists(path):
        if "/" in path and platform.system() == "Windows":
            path = path.replace("/", "\\")
        path = os.path.join(BASE_PATH, path)
        if not os.path.isfile(path):
            raise FileNotFoundError("文件不存在 ==>> {}".format(path))
    return path


def get_csv_path(path: str, file_name: str) -> str:
    """
    返回csv文件完整路径
    :param path:
    :param file_name:
    :return:
    """
    if os.path.isfile(file_name):
        csv_path = file_name
    else:
        csv_path = path.replace("data.yml", file_name)
    return check(csv_path)


def fun_name() -> str:
    """
    返回当前执行的函数名称
    :return:
    """
    return inspect.stack()[1][3]


def error_msg(field: str) -> str:
    """
    断言失败提示
    :param field:
    :return:
    """
    msg = f"接口返回字段 {field} 断言错误！"
    return msg


def file_obj(file_name: str, path: str):
    """
    判断上传文件绝对路径
    :param file_name: 上传文件名称 or 路径
    :param path: 测试数据路径
    :return:
    """
    if os.path.exists(file_name) and os.path.isfile(file_name):
        abs_path = file_name
    else:
        abs_path = path.replace("data.yml", file_name)
    return io.open(abs_path, "rb")


def get_data_path(path: str) -> str:
    """
    返回完整的data.yml文件路径
    :param path: 当前执行用例的路径
    :return:
    """
    data_path = os.path.join(path, "data", "data.yml")
    return check(data_path)


def get_project_name(path: str) -> str:
    """
    返回 project_name
    :param path: 执行文件路径
    :return:
    """
    path_list = path.split(patt)
    project_name = path_list[-2]
    return project_name


def mkdir(path) -> str:
    """
    检查目录是否存在，不存在则创建
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)
    return path


# 日志文件路径
LOG_PATH = mkdir(os.path.join(BASE_PATH, "log"))
# 配置文件路径
CONFIG_PATH = check(os.path.join(BASE_PATH, "config", "setting.ini"))
# 报告目录
REPORT_PATH = mkdir(os.path.join(BASE_PATH, "report"))
# case目录
CASE_PATH = mkdir(os.path.join(BASE_PATH, "testcase"))
# 格式化时间
format_time = time.strftime("%Y-%m-%d")
format_time_min = time.strftime("%Y%m%d%H%M")
