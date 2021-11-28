#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: exceptions.py
# 说   明: 
# 创建时间: 2021/11/5 23:18
# @Version：V 0.1
# @desc :

class MyBaseError(Exception):
    """异常基类"""
    pass


class FileFormatError(MyBaseError):
    """文件格式化错误"""
    pass


class FileTypeNotEmptyOrYamlError(MyBaseError):
    """文件写入时文件类型不能为空和YAML文件"""
    pass


class ExtractParamsError(MyBaseError):
    """参数提取错误"""
    pass


class DBConnectError(MyBaseError):
    """数据库连接错误"""
    pass


class QuerySqlError(MyBaseError):
    """查询sql命名或者对应关系错误"""
    pass


class ParametrizeValidateError(MyBaseError):
    """参数化断言YAML配置错误"""
    pass


class InterfaceRequestError(MyBaseError):
    """接口请求出现异常"""
    pass


class CSVFormatError(MyBaseError):
    """csv文件数据格式异常"""
    pass
