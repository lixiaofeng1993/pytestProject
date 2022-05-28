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


@pytest.fixture(scope="session", autouse=True)
def test_token():
    read = ReadFileData()
    host = read.get_host()
    url = host + "/users/login"
    data = {
        "username": "lixiaofeng",
        "password": "123456"
    }
    res = requests.post(url, data)
    data = json.loads(decrypt(res.json().get("result")))
    token = data.get("access_token")
    if token:
        os.environ["token"] = token
#