#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: random_params.py
# 说   明: 
# 创建时间: 2021/11/21 0:37
# @Version：V 0.1
# @desc :


import re
import random
from faker import Faker
from datetime import datetime

faker = Faker('zh_CN')


def batch_replace(data, index, original_list, replace_list):
    """
    批量替换
    :param data:
    :param index:
    :param replace_list:
    :param original_list:
    :return:
    """
    data = data.replace(original_list[index], replace_list[index])
    return data


def fake_params(params, value, key='', i=0):
    """
    支持对参数中存在的嵌套参数进行参数化
    :param params: 参数字典
    :param value: 包含参数化关键字的值
    :param key: 字典的key，区分dict、list
    :param i: list参数包含关键字的位置
    :return:
    """
    if isinstance(value, str):
        if '__random_int' in value:
            regexp = r"(\(.+?\))"
            regexp1 = r"\((.+?)\)"
            value_list = re.findall(regexp, value)
            value_list1 = re.findall(regexp1, value)
            if value_list and len(value_list) == len(value_list1):
                replace_list = []
                original_list = []
                for i in range(len(value_list)):
                    try:
                        k = int(value_list1[i].split(',')[0])
                        v = int(value_list1[i].split(',')[1])
                        replace_list.append(str(random.randint(k, v)))
                        original_list.append('__random_int' + value_list[i])
                    except ValueError:
                        return 'error'
                for i in range(len(value_list)):
                    value = batch_replace(value, i, original_list, replace_list)
                if key:
                    params[key] = value
                elif isinstance(params, list):
                    params.remove(value)
                    params.insert(i, value)
                else:
                    for i in range(len(value_list)):
                        params = batch_replace(params, i, original_list, replace_list)
            else:
                params[key] = random.randint(1, 10000)
        elif '__cent' in value:  # 金额 元 转 分
            regexp = r"\((.+?)\)"
            cent_list = re.findall(regexp, value)
            if cent_list and cent_list[0].replace(".", '').isdigit():
                params[key] = float(cent_list[0]) * 100
        elif '__name' in value:
            str_value = value.split('__name')[0]
            str_value1 = value.split('__name')[1]
            str_name = faker.name()
            if key:
                params[key] = str_value + str_name + str_value1
            else:
                params.remove(value)
                params.insert(i, str_value + str_name + str_value1)
        elif '__address' in value:
            str_value = value.split('__address')[0]
            str_value1 = value.split('__address')[1]
            str_address = faker.address()
            if key:
                params[key] = str_value + str_address + str_value1
            else:
                params.remove(value)
                params.insert(i, str_value + str_address + str_value1)
        elif '__phone' in value:
            str_value = value.split('__phone')[0]
            str_value1 = value.split('__phone')[1]
            str_phone = faker.phone_number()
            if key:
                params[key] = str_value + str_phone + str_value1
            else:
                params.remove(value)
                params.insert(i, str_value + str_phone + str_value1)
        elif '__text' in value:
            regexp = r"\((.+)\)"
            num = re.findall(regexp, value)
            str_value = value.split('__text')[0]
            str_value1 = value.split('__text')[1]
            if num:
                try:
                    number = int(num[0])
                    if key:
                        params[key] = str_value + faker.text(max_nb_chars=number).replace('\n', '').replace('\r', '')
                    else:
                        params.remove(value)
                        params.insert(i,
                                      str_value + faker.text(max_nb_chars=number).replace('\n', '').replace('\r', ''))
                except ValueError:
                    return 'error'
            else:
                if key:
                    params[key] = str_value + faker.text().replace('\n', '').replace('\r', '') + str_value1
                else:
                    params.remove(value)
                    params.insert(i, str_value + faker.text().replace('\n', '').replace('\r', '') + str_value1)
        elif '__word' in value:
            str_value = value.split('__word')[0]
            str_value1 = value.split('__word')[1]
            if key:
                params[key] = str_value + faker.word().replace('\n', '').replace('\r', '') + str_value1
            else:
                params.remove(value)
                params.insert(i, str_value + faker.word().replace('\n', '').replace('\r', '') + str_value1)
        elif '__random_time' in value:
            regexp = r"\((.+)\)"
            tag = re.findall(regexp, value)
            str_value = value.split('__random_time')[0]
            str_value1 = value.split('__random_time')[1]
            str_random_time = faker.date_time()
            if tag:
                if tag[0].lower() == 'd':
                    if key:
                        params[key] = str_value + str(str_random_time)[:10]
                    else:
                        params.remove(value)
                        params.insert(i, str_value + str(str_random_time)[:10])
                else:
                    if key:
                        params[key] = str_value + str(str_random_time)
                    else:
                        params.remove(value)
                        params.insert(i, str_value + str(str_random_time))
            else:
                if key:
                    params[key] = str_value + str(str_random_time) + str_value1
                else:
                    params.remove(value)
                    params.insert(i, str_value + str(str_random_time) + str_value1)
        elif '__now' in value:
            regexp = r"\((.+)\)"
            tag = re.findall(regexp, value)
            str_value = value.split('__now')[0]
            str_value1 = value.split('__now')[1]
            str_random_time = datetime.now()
            if tag:
                if tag[0].lower() == 'd':
                    if key:
                        params[key] = str_value + str(str_random_time)[:10]
                    else:
                        params.remove(value)
                        params.insert(i, str_value + str(str_random_time)[:10])
                else:
                    if key:
                        params[key] = str_value + str(str_random_time)[:-7]
                    else:
                        params.remove(value)
                        params.insert(i, str_value + str(str_random_time)[:-7])
            else:
                if key:
                    params[key] = str_value + str(str_random_time)[:-7] + str_value1
                else:
                    params.remove(value)
                    params.insert(i, str_value + str(str_random_time)[:-7] + str_value1)
        elif '__email' in value:
            str_value = value.split('__email')[0]
            str_value1 = value.split('__email')[1]
            str_email = faker.email()
            if key:
                params[key] = str_value + str_email + str_value1
            else:
                params.remove(value)
                params.insert(i, str_value + str_email + str_value1)
        return params


def random_params(params: (dict, list, str)):
    """
    随机参数化
    :param params:
    :return:
    """
    if isinstance(params, dict):
        for key, value in params.items():
            if isinstance(value, (dict, list)):
                random_params(value)
            elif isinstance(value, str):
                fake_params(params, value, key)
    elif isinstance(params, list):
        for i in range(len(params)):
            if isinstance(params[i], (dict, list)):
                random_params(params[i])
            elif isinstance(params[i], str):
                fake_params(params, params[i])
    elif isinstance(params, str):
        params = fake_params(params, params)
    return params
