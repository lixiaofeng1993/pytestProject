#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: conftest.py
# 说   明: 
# 创建时间: 2022/5/25 15:06
# @Version：V 0.1
# @desc :
import json

import pytest
import requests
import os

from public.read_data import ReadFileData
from public.sign import decrypt
from public.log import logger


@pytest.fixture(scope="session", autouse=True)
def test_token():
    read = ReadFileData()
    host = read.get_host()
    login_url = host + "/users/login"
    login_data = {
        "username": "lixiaofeng",
        "password": "123456"
    }
    # 登录获取token
    login_res = requests.post(login_url, login_data)
    data = json.loads(decrypt(login_res.json().get("result")))
    token = data.get("access_token")
    if token:
        logger.info(f"登录接口 -->> token：{token}")
        os.environ["token"] = token
    yield
    # 退出登录
    logout_url = host + "/users/logout"
    logout_headers = {
        "Authorization": f"Bearer {token}"
    }
    logout_res = requests.post(logout_url, headers=logout_headers)
    logger.info(f"退出登录接口 -->> 返回值： {logout_res.json()}")
