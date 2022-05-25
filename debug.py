#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: debug.py
# 说   明: 
# 创建时间: 2022/4/27 19:41
# @Version：V 0.1
# @desc :
import io
import csv
import os.path

from public.help import check, CASE_PATH
from public import exceptions
from public.sign import encrypt, encrypt_md5, decrypt


def username():
    return 'lixiaofeng'


def password():
    return "123456"


def token():
    return os.getenv("token")


def load_csv(file_path: str) -> list:
    """
    读取参数化csv文件数据
    :param file_path: 文件路径
    :return:
    """
    file_path = os.path.join(CASE_PATH, file_path)
    parametrize_list = list()
    # logger.info(f"加载 {file_path} 文件......")
    with io.open(check(file_path), encoding='gbk') as f:
        reader = csv.DictReader(f)
        for value in reader:
            parametrize = list()
            # del value["case_name"]
            validate_list = list()
            params_list = list()
            try:
                key = ",".join(value.keys()).strip()
                key_list = key.split(",,")
            except Exception as error:
                raise exceptions.CSVFormatError(f"csv文件数据格式异常！{error}")
            if len(key_list) == 1:
                params_list.append(value)
                parametrize.append(params_list)
            elif len(key_list) == 2:
                params_key_list = key_list[0]
                validate_key_list = key_list[1]
                for k, v in value.items():
                    if k and k in params_key_list:
                        parametrize.append({k: v})
                    elif k and k in validate_key_list:
                        if v:
                            validate_value = eval(v)
                            validate_value.update({"check": k})
                            validate_list.append([validate_value])
                parametrize.append({"validate": validate_list})
            else:
                raise exceptions.CSVFormatError("csv文件数据格式异常！")
            parametrize_list.append(parametrize)
    # logger.info(f"读到数据 ==>>  {parametrize_list} ")
    return parametrize_list
