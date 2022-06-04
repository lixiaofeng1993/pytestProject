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

from public.exceptions import ResponseError


def decrypt(data: str) -> str:
    """
    AES 解密
    :param data: 要解密的数据
    :return:
    """
    key = b"nsz3*H&I@xINg/tH"
    patt = "([\\[{].+[\\]}])"
    try:
        data = binascii.a2b_hex(data)
        aes = AES.new(key, AES.MODE_ECB)
        data = aes.decrypt(data)
        data = data.decode('utf-8').strip('\t')
        data = re.findall(patt, data)[0]
    except TypeError as error:
        raise ResponseError(f"接口返回值 {data} 解密出现异常 -->> {error}")
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
    data = decrypt("a2ddfdd3039ab3cd9110af5eee87aea35ecd8b67a7dec296e196212705f65ee7a4f6b3edb2cc3f755429ea988497b45cc4dc2c31ba8e012870aa6236189e9cf675c2c2a4db857241281aa79e9395362a8e68b58e94a61b2c11f239588ca5a6d82d236cf9e2ea3f0784fd469ea1e4ef015af180b8effaaa01e7d724dd9d35263c8d960a0d33684a1151d2ca2acf401a64a5b52f98016b5f454881e430fb3fcdf99ff0d6156a2dd07a4987161e2b47fd6fd46ff269fa973426190d4743955e96533b7effcc793fbef10b54a5bcb3d27184ebb7e0b7428948a83441cd8c5ca9e75cc73d99bcdf81aec3f48ef1050a4d4fb6cd648d2bc30900697cf7f42a3a3fb94a441783db1ba3211eccc121fb8452f40459d594fcadf7eff1cf990b480490eda249a09e938695dfa4bde50732fe9e7ddb014f36fa1195cd99615680760745fa44345b011810522de64ca3ddc5ff2924aa60d914e45bc2b88479bff9304577d12c675b5dabd84530390851c3aed580d6ffaa7e2df1dc94b3a1582236d9ff244d995b810f86c9fae17383e18f932d1f2e56bc6ffe008d575d492e56a424ed06075da2ac907eb96aec32fa715e26f5ad1fc62245a370af979a484c42d10130a5a207eabd31b30e2c5564f22ba52a3bf2abc40711a96eb0d58ecf6b0d8b342b443defcc09f6fc2c54fdf8bfa4dab79fe36e740f568ca6dde03e0adeba084aba6e0a154d4c78a241c68ee79821dc65f63303d0acf76704ad88bab2fde367ba9a2fa855")
    print(data)
