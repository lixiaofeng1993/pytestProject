#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pytestProject 
@File ：common.py
@Author ：李永峰
@Date ：2021/11/4 10:56 
@Version：1.0
@Desc：
"""

import re
from jsonpath import jsonpath
from public.log import logger
from public.oracle_operate import OracleDb
from public.mysql_operate import MysqlDb
from public.random_params import random_params
from public import exceptions
from public.help import file_obj, error_msg, get_csv_path
from public.read_data import ReadFileData
from requests_toolbelt import MultipartEncoder


def replace_variable(real_value, patt_value, data_value, value, key=None):
    """
    替换上下文依赖和查询数据库的值
    :param real_value: 遍历后值是字符串
    :param patt_value: 正则匹配到的值
    :param data_value: 遍历的测试数据
    :param key: 遍历的测试数据是字典的情况
    :param value: 遍历后值是字符串
    :return: 替换后的数据
    """
    if real_value:
        var_value = real_value if isinstance(real_value, str) else str(real_value)
        if isinstance(data_value, dict):
            data_value[key] = data_value[key].replace(patt_value, var_value, 1)
        elif isinstance(data_value, list):
            index = data_value.index(patt_value)
            data_value.remove(value)
            data_value.insert(index, var_value)
        if isinstance(data_value, str):
            data_value = data_value.replace(patt_value, var_value, 1)
        # logger.info(f"提取替换的数据 ==>> {patt_value} -> {var_value}")
        return data_value


def query_replace_variable(value, variables, data_value, key=None, data_type="str", file_path=None):
    """
    查询上下文依赖和数据库的值
    :param value: 遍历后值是字符串
    :param variables: 需要查询替换的变量
    :param data_value: 遍历的测试数据
    :param key: 遍历的测试数据是字典的情况
    :param data_type: sql查询返回的数据类型
    :param file_path: csv参数化文件路径
    :return: 替换后的数据
    """
    variable_regexp = r"(\$[\w_\+]+)"
    patt = re.findall(variable_regexp, value)
    # csv_regexp = r"\${([\w_\.csv]+)}" # 递归替换yml文件中引用csv文件数据，被jinja2方式取代
    # csv_patt = re.findall(csv_regexp, value)
    # real_value = ""
    # if csv_patt:
    #     for csv_value in csv_patt:  # csv参数化数据替换
    #         if csv_value:
    #             _value_list = csv_value.split(".")
    #             if _value_list[-1] != "csv":
    #                 raise exceptions.ParametrizeValidateError("csv 参数化文件名称配置错误！")
    #             csv_path = get_csv_path(file_path, csv_value)
    #             read = ReadFileData()
    #             real_value = read.load_csv(csv_path)
    #         data_value[key] = real_value
    #         # logger.info(f"提取替换的数据 ==>> {key} -> {real_value}")
    #         return data_value
    if variables:
        if "sql_" in value:  # sql查询替换
            if value[:3] != "sql":
                sql_regexp = r"(sql_[\w_]+)"
                value = re.findall(sql_regexp, value)[0] if re.findall(sql_regexp, value) else None
            try:
                db_type = variables.get("db_type")
                if db_type == "oracle":
                    db = OracleDb()
                else:
                    db = MysqlDb()
                sql = variables[value]
                real_value = db.execute_db(sql, data_type=data_type)
                patt_value = value
                data_value = replace_variable(real_value, patt_value, data_value, value, key)
            except Exception as error:
                raise exceptions.QuerySqlError(f"查询sql命名或者对应关系错误 ==>> {error}")
        elif patt:
            for patt_value in patt:
                _value = patt_value.strip("$")
                real_value = variables.get(_value)
                data_value = replace_variable(real_value, patt_value, data_value, value, key)
        return data_value


def recursion_handle(data_value, variables, file_path=None):
    """
    递归遍历测试数据
    :param data_value: 测试数据
    :param variables:  替换的查询数据
    :param file_path:  csv参数化文件路径
    :return:
    """
    if isinstance(data_value, dict):
        for key, value in data_value.items():
            if key != "jsonpath":
                if isinstance(value, str):
                    query_replace_variable(value, variables, data_value, key, file_path=file_path)
                else:
                    recursion_handle(value, variables, file_path)
    elif isinstance(data_value, list):
        for i in range(len(data_value)):
            if isinstance(data_value[i], str):
                query_replace_variable(data_value[i], variables, data_value, file_path=file_path)
            else:
                recursion_handle(data_value[i], variables, file_path)
    elif isinstance(data_value, str):
        data_value = query_replace_variable(data_value, variables, data_value, file_path=file_path)
    data_value = random_params(data_value)
    return data_value


def extract_variables(res, extract: dict, variables: dict) -> dict:
    """
    从返回值中提取参数值，并添加到全局变量中
    :param res: 接口返回值
    :param variables: 包含extract信息的测试数据
    :param extract: 全局变量
    :return:
    """
    if extract and isinstance(extract, dict):
        for key, value in extract.items():
            ext_value = jsonpath(res, value)
            logger.info(f"从返回值中提取的参数 路径 值 ==>> {key}:{value} -> {ext_value}")
            # if not ext_value:
            #     msg = f"提取路径未从返回值中提取到指定值！{key}:{value}"
            #     raise exceptions.ExtractParamsError(msg)
            value = ext_value[0] if ext_value else None
            variables.update({
                key: value
            })
    return variables


def upload_file(upload: list, file_path: str):
    """
    上传文件
    :param upload:
    :param file_path:
    :return:
    """
    _upload = dict()
    for i in range(len(upload)):
        _upload[f"files{i}"] = (upload[i], file_obj(upload[i], file_path))
    m = MultipartEncoder(_upload)
    return m


def parametrize_validate(parametrize):
    """
    处理参数化数据
    :param parametrize: 接口参数化数据
    :return:
    """
    params = dict()
    validate = []
    for param in parametrize:
        if isinstance(param, dict):
            for key, value in param.items():
                if key == "validate":
                    validate = value
                elif key != "case_name":
                    params.update(param)
    return validate, params


def default_extract(res, field: str) -> str:
    """
    默认获取返回值中同期望字段的值
    :param res:
    :param field:
    :return:
    """
    real_field = ""
    if isinstance(res, dict):
        if field in res.keys():
            real_field = res[field]
        else:
            for value in res.values():
                default_extract(value, field)
    elif isinstance(res, list):
        for key in res:
            default_extract(key, field)
    return real_field


def not_empty(date):
    """
    关键字段值不为空判断
    :param date:
    :return:
    """
    if date:
        return date
    raise exceptions.NotEmptyError("YAML数据字段不能为空！")


def validators_result(result, validate: list):
    """
    断言
    :param result:
    :param validate:
    :return:
    """
    try:
        validate = validate if validate and validate[0] else []
    except (IndexError, KeyError):
        validate = []
    response = result.text
    checkpoint_list = list()
    if not validate:
        checkpoint_list = [{"comparator": "equal", "check": "status_code", "expect": "200", "jsonpath": ""}]
    elif isinstance(validate, list):
        for val in validate:
            checkpoint = dict()
            if isinstance(val, list):
                for v in val:
                    checkpoint.update(v)
            checkpoint_list.append(checkpoint)
    for checkpoint in checkpoint_list:
        if isinstance(checkpoint, dict):
            comparator = checkpoint["comparator"] if checkpoint.get("comparator") else ""
            check = checkpoint.get("check")
            expect = checkpoint.get("expect")
            path = checkpoint["jsonpath"] if checkpoint.get("jsonpath") else ""
            if check == "status_code":
                check_field = result.status_code
            elif path:
                check_field = jsonpath(response, path)
            else:
                check_field = default_extract(response, check)
            logger.info(f"断言方式：{comparator} 断言字段：{check} ==>> 断言值：{expect} ==>> 期望值：{check_field}")
            expect = expect if isinstance(expect, str) else str(expect)
            if comparator == "equal":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert field == expect, error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert check_field == expect, error_msg(check)
            elif comparator == "not_equal":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert field != expect, error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert check_field != expect, error_msg(check)
            elif comparator == "contains":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert expect in field, error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert expect in check_field, error_msg(check)
            elif comparator == "notcontains":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert expect in field, error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert expect not in check_field, error_msg(check)
            elif comparator == "startswith":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert field.startswith(expect), error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert check_field.startswith(expect), error_msg(check)
            elif comparator == "endswith":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert field.endswith(expect), error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert check_field.endswith(expect), error_msg(check)
            elif comparator == "greater_than":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert field > expect, error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert check_field > expect, error_msg(check)
            elif comparator == "less_than":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert field < expect, error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert check_field < expect, error_msg(check)
            elif comparator == "greater_or_equals":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert field >= expect, error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert check_field >= expect, error_msg(check)
            elif comparator == "less_or_equals":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert field <= expect, error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert check_field <= expect, error_msg(check)
            elif comparator == "regex_match":
                if isinstance(check_field, list):
                    for field in check_field:
                        field = str(field) if not isinstance(field, str) else field
                        assert re.match(expect, field), error_msg(check)
                else:
                    check_field = check_field if isinstance(check_field, str) else str(check_field)
                    assert re.match(expect, check_field), error_msg(check)
            logger.info(f"断言成功！")
