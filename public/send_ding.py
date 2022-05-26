#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: send_ding.py
# 说   明: 
# 创建时间: 2022/5/26 9:46
# @Version：V 0.1
# @desc :
import hmac
import urllib.parse
import hashlib
import base64
import requests
import urllib3
import time

from public.log import logger
from public.read_data import ReadFileData

urllib3.disable_warnings()
read = ReadFileData()


def ding_sign():
    """
    发送钉钉消息加密
    :return:
    """
    timestamp = str(round(time.time() * 1000))
    secret = "SEC07e54da76a6e625967991b7d33eb422667abe5be81c9b94161b766773105a423"
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def send_ding(plugin):
    """
    发送钉钉消息
    :param plugin:
    :return:
    """
    headers = {"Content-Type": "application/json"}
    access_token = "fe86177bed3761d722b2d9deefeb68577e820142474c970796ec576e0680605d"
    timestamp, sign = ding_sign()
    # 发送内容
    summary = plugin.report.get("summary")
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)
    total = summary.get("total", 0)
    duration = plugin.report.get("duration", None)
    start = time.localtime(plugin.report["created"] if plugin.report.get("created", None) else time.time())
    start = time.strftime("%Y-%m-%d %H:%M:%S", start)
    body = {
        "msgtype": "text",
        "text": {
            "content": f"接口测试报告 开始时间 {start}，持续时长 {duration} 秒。\n 共 {total} 条，通过 {passed} 条，"
                       f"失败 {failed} 条，跳过 {skipped} 条.\n 详情请前往框架 report 目录查看。"
        }
    }
    ding = read.get_system().get("ding", None)
    if ding == "true":
        res = requests.post(
            "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(
                access_token, timestamp, sign), headers=headers, json=body, verify=False).json()
        if res["errcode"] == 0 and res["errmsg"] == "ok":
            logger.info("钉钉通知发送成功！info：{}".format(body["text"]["content"]))
        else:
            logger.error("钉钉通知发送失败！返回值：{}".format(res))
