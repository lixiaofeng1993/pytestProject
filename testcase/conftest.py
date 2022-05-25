#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: conftest.py
# 说   明: 
# 创建时间: 2022/5/25 15:06
# @Version：V 0.1
# @desc :
import pytest
import requests
import os


@pytest.fixture(scope="session", autouse=True)
def test_token():
    url = "http://121.41.54.234/users/login"
    data = {
        "username": "lixiaofeng",
        "password": "123456"
    }
    res = requests.post(url, data)
    token = res.json().get("access_token")
    if token:
        os.environ["token"] = token
