#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: sign.py
# 说   明: 
# 创建时间: 2022/5/3 10:45
# @Version：V 0.1
# @desc : 解密AES加密接口返回值
from Crypto.Cipher import AES
import binascii
import hashlib
import datetime
import re


def decrypt(data: str) -> str:
    """
    AES 解密
    :param data: 要解密的数据
    :return:
    """
    key = b"nsz3*H&I@xINg/tH"
    patt = "([\\[{].+[\\]}])"
    data = binascii.a2b_hex(data)
    aes = AES.new(key, AES.MODE_ECB)
    data = aes.decrypt(data)
    data = data.decode('utf-8').strip('\t')
    data = re.findall(patt, data)[0]
    return data


def add_to_16(text: str) -> str:
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


def encrypt(data: str) -> str:
    """
    AES 加密
    :param data: 要解密的数据
    :return:
    """
    key = b"nsz3*H&I@xINg/tH"
    aes = AES.new(key, AES.MODE_ECB)
    data = aes.encrypt(add_to_16(data))
    return binascii.b2a_hex(data).decode()


def encrypt_md5():
    """
    对向前日期进行md5加密
    """
    now = datetime.datetime.now().strftime('%Y%m%d')
    h = hashlib.md5()
    h.update(now.encode(encoding='utf-8'))
    return h.hexdigest()


if __name__ == '__main__':
    data = encrypt("17666666666")
    print(data)
