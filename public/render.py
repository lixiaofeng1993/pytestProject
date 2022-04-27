#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: render.py
# 说   明: 
# 创建时间: 2022/4/27 19:47
# @Version：V 0.1
# @desc : 动态加载替换yml文件中的函数

import os
import jinja2
import importlib
import inspect


def render(tpl_path, **kwargs):
    """渲染yml文件"""
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')
                              ).get_template(filename).render(**kwargs)


def all_functions():
    """加载debug.py模块"""
    debug_module = importlib.import_module("debug")
    all_function = inspect.getmembers(debug_module, inspect.isfunction)
    return dict(all_function)
