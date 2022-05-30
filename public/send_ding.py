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


def send_ding(terminalreporter):
    """
    发送钉钉消息
    :param plugin:
    :return:
    # from pytest_jsonreport.plugin import JSONReport
    # summary = plugin.report.get("summary")
    # passed = summary.get("passed", 0)
    # failed = summary.get("failed", 0)
    # skipped = summary.get("skipped", 0)
    # total = summary.get("total", 0)
    # duration = str(plugin.report.get("duration", None))[:-12]
    # start = time.localtime(plugin.report["created"] if plugin.report.get("created", None) else time.time())
    # start = time.strftime("%Y-%m-%d %H:%M:%S", start)
    """
    headers = {"Content-Type": "application/json"}
    access_token = "fe86177bed3761d722b2d9deefeb68577e820142474c970796ec576e0680605d"
    timestamp, sign = ding_sign()
    # 发送内容
    total = terminalreporter._numcollected
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    rate = passed / total * 100
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    system = read.get_system()
    flag = read.get_flag()
    url = system.get("allure_test_url", None) if flag == "0" else system.get("allure_url", None)
    ding = system.get("ding", None)
    body = {
        "msgtype": "text",
        "text": {
            "content": f"接口测试报告 持续时长 {str(duration)[:-12]} 秒。\n 用例共 {total} 条，通过 {passed} 条，"
                       f"失败 {failed} 条，错误 {error} 条，跳过 {skipped} 条，成功率 {rate} %.\n 详情前往地址：{url} 查看。"
        }
    }
    if ding == "true":
        res = requests.post(
            "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(
                access_token, timestamp, sign), headers=headers, json=body, verify=False).json()
        if res["errcode"] == 0 and res["errmsg"] == "ok":
            logger.info("钉钉通知发送成功！info：{}".format(body["text"]["content"]))
        else:
            logger.error("钉钉通知发送失败！返回值：{}".format(res))
