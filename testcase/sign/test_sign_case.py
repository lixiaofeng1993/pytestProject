#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: test_sign_case.py
# 说   明: 
# 创建时间: 2022/5/3 10:44
# @Version：V 0.1
# @desc :
import pytest
from public.send_request import SendRequest
from public.log import logger
from public.sql_to_data import SqlToData
from public.help import get_data_path, os, fun_name, report_setting, report_step_setting, allure

data_path = get_data_path(os.path.dirname(__file__))
test_params = SqlToData().yaml_db_query(data_path)


@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic(test_params.get("epic"))
@allure.feature(test_params.get("feature"))
class TestSignCase:

    def setup_class(self):
        self.extract = {}

    def test_sign_case(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        # 报告展示的测试步骤
        report_step_setting(test_data)
        # 登录接口
        result, self.extract = SendRequest(test_data, self.extract).send_request()

        # 报告上展示的测试标题等
        report_setting(test_data)
        logger.info("*************** 结束执行用例 ***************\n")

    def test_token_case(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        # 报告展示的测试步骤
        report_step_setting(test_data)
        # 登录接口
        result, self.extract = SendRequest(test_data, self.extract).send_request()

        # 报告上展示的测试标题等
        report_setting(test_data)
        logger.info("*************** 结束执行用例 ***************\n")

    def test_getoperateinfo_case(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        # 报告展示的测试步骤
        report_step_setting(test_data)

        result, self.extract = SendRequest(test_data, self.extract).send_request()

        # 报告上展示的测试标题等
        report_setting(test_data)
        logger.info("*************** 结束执行用例 ***************\n")


if __name__ == '__main__':
    pytest.main(
        ["-q", "-s", "test_sign_case.py", "-W", "ignore:Module already imported:pytest.PytestWarning"])
