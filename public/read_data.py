#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: read_data.py
# 说   明: 
# 创建时间: 2021/11/2 23:04
# @Version：V 0.1
# @desc : 数据读取
import yaml
import csv
import json
from configparser import ConfigParser
from public.render import render, all_functions
from public.log import logger
from public.help import *


class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class ReadFileData:

    def __init__(self):
        pass

    def load_yaml(self, file_path: str) -> dict:
        """
        加载yml文件数据
        :param file_path: 文件路径
        :return:
        """
        # logger.info(f"加载 {file_path} 文件......")
        f = render(file_path, **all_functions())
        data = yaml.safe_load(f)
        # with open(check(file_path), encoding='utf-8') as f:
        #     try:
        #         data = yaml.safe_load(f)
        #     except yaml.YAMLError as ex:
        #         raise exceptions.FileFormatError("file: {} error: {}".format(file_path, ex))
        # logger.info(f"读到数据 ==>>  {data} ")
        return data

    def load_json(self, file_path: str) -> (dict or list):
        """
        加载json文件数据
        :param file_path: 文件路径
        :return:
        """
        logger.info(f"加载 {file_path} 文件......")
        with open(check(file_path), encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as ex:
                raise exceptions.FileFormatError("file: {} error: {}".format(file_path, ex))
        logger.info(f"读到数据 ==>>  {data} ")
        return data

    def load_ini(self, file_path: str) -> dict:
        """
        加载ini配置文件数据
        :param file_path: 文件路径
        :return:
        """
        # logger.info(f"加载 {file_path} 文件......")
        config = MyConfigParser()
        config.read(check(file_path), encoding="UTF-8")
        data = dict(config._sections)
        # logger.info(f"读到数据 ==>>  {data} ")
        return data

    def load_csv(self, file_path: str) -> list:
        """
        读取参数化csv文件数据
        :param file_path: 文件路径
        :return:
        """
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

    def write_file(self, file_path: str, data="", file_type: str = "zip", file_name: str = "") -> None:
        """
        下载文件接口返回的文件流写入文件中
        :param file_path: 文件路径
        :param data: 写入数据
        :param file_type: 写入文件类型 文件后缀
        :param file_name: 指定文件名称
        :return:
        """
        dir_path, fullflname = os.path.split(check(file_path))
        if not file_type:
            raise exceptions.FileTypeNotEmptyOrYamlError("写入文件类型不能为空！")
        elif file_type == "yml":
            raise exceptions.FileTypeNotEmptyOrYamlError("写入文件类型不能是YAML文件！")
        else:
            write_file_path = os.path.join(dir_path, f"{file_name}-{format_time_min}.{file_type}")
        logger.info("写入 文件 {} 数据 {}.".format(file_path, data))
        with io.open(write_file_path, "wb") as f:
            f.write(data)

    def load_setting_ini(self) -> dict:
        """
        加载 setting.ini 文件
        :return:
        """
        data = self.load_ini(CONFIG_PATH)
        return data

    def get_mysql_config(self) -> dict:
        """
        返回mysql数据库配置信息
        :return:
        """
        data = self.load_setting_ini()["mysql"]
        db_conf = {
            "host": data["MYSQL_HOST"],
            "port": int(data["MYSQL_PORT"]),
            "user": data["MYSQL_USER"],
            "password": data["MYSQL_PASSWD"],
            "db": data["MYSQL_DB"]
        }
        return db_conf

    def get_oracle_config(self) -> dict:
        """
        返回oracle数据库配置信息
        :return:
        """
        data = self.load_setting_ini()["oracle"]
        db_conf = {
            "dsn": data["oracle_dns"],
            "port": data["oracle_port"],
            "user": data["oracle_usr"],
            "password": data["oracle_pwd"],
        }
        return db_conf

    def get_host(self) -> str:
        """
        默认返回测试环境host
        :return:
        """
        data = self.load_setting_ini()["host"]
        host = data["test_host"]
        return host

    def get_variable(self) -> dict:
        """
        返回固定变量
        :return:
        """
        variable = self.load_setting_ini()["variable"]
        variable = dict(variable) if variable else {}
        return variable


if __name__ == '__main__':
    data = ReadFileData()
    print(data.load_yaml(r"E:\project\pytestProject\testcase\users\data\data.yml"))
