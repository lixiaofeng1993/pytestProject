#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pytestProject 
@File ：sql_to_data.py
@Author ：李永峰
@Date ：2021/11/3 12:50 
@Version：1.0
@Desc：参数化中需要从数据库替换值的情况；
"""

from public.read_data import ReadFileData
from public.log import logger
from public.common import recursion_handle
from base.object_data import object_data


class SqlToData:

    def __init__(self, data_type: str = "str"):
        self.read = ReadFileData()
        self.data_type = data_type

    def yaml_db_query(self, file_path: str):
        """
        返回处理过的yaml数据
        :param file_path: 文件路径
        :return:
        """
        test_data = self.read.load_yaml(file_path)
        sql_data = test_data.get("sql")
        if sql_data:
            del test_data["sql"]
        # for keys, data_value in test_data.items():
        #     recursion_handle(data_value, {}, file_path=file_path)
        if sql_data:
            for keys, data_value in test_data.items():
                recursion_handle(data_value, sql_data)
        case_step_num = self.read.get_variable().get("case_step_num")
        test_data = object_data(test_data, file_path, case_step_num)
        # logger.info(f"更新后的数据：{test_data}")
        return test_data


if __name__ == '__main__':
    data = SqlToData()
