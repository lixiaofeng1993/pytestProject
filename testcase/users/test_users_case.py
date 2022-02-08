#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: test_users_case.py
# 说   明: 
# 创建时间: 2021/11/27 19:16
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
class TestUsersCase:

    def setup_class(self):
        self.extract = {}

    # @pytest.mark.parametrize("data", test_params["test_register_user_case"].parametrize)
    # def test_register_user_case(self, data):
    #     logger.info("*************** 开始执行用例 ***************")
    #     # 获取执行用例函数名
    #     name = fun_name()
    #     # 报告展示的测试步骤
    #     report_step_setting(test_params[name])
    #
    #     test_params[name].parametrize = data
    #     result, self.extract = SendRequest(test_params[name], self.extract).send_request()
    #
    #     # 报告上展示的测试标题等
    #     report_setting(test_params[name])
    #     logger.info("*************** 结束执行用例 ***************\n")

    @pytest.mark.parametrize("data", test_params["test_one_user_case"].parametrize)
    def test_one_user_case(self, data):
        logger.info("*************** 开始执行用例 ***************")
        # 获取执行用例函数名
        name = fun_name()
        # 报告展示的测试步骤
        report_step_setting(test_params[name].case_step_1)

        # 登录接口
        result, self.extract = SendRequest(test_params[name].case_step_1, self.extract).send_request()

        report_step_setting(test_params[name])
        test_params[name].parametrize = data
        result, self.extract = SendRequest(test_params[name], self.extract).send_request()

        # 报告上展示的测试标题等
        report_setting(test_params[name])
        logger.info("*************** 结束执行用例 ***************\n")

    def test_all_user_case(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        # 报告展示的测试步骤
        report_step_setting(test_data.case_step_1)
        # 登录接口
        result, self.extract = SendRequest(test_data.case_step_1, self.extract).send_request()

        report_step_setting(test_data.case_step_2)
        result, self.extract = SendRequest(test_data.case_step_2, self.extract).send_request()

        # 报告上展示的测试标题等
        report_setting(test_data.case_step_2)
        logger.info("*************** 结束执行用例 ***************\n")

    def test_delete_user_case(self, test_data):
        logger.info("*************** 开始执行用例 ***************")

        report_step_setting(test_data.case_step_1)
        result, self.extract = SendRequest(test_data.case_step_1, self.extract).send_request()

        report_step_setting(test_data.case_step_2)
        result, self.extract = SendRequest(test_data.case_step_2, self.extract).send_request()

        report_step_setting(test_data.case_step_3)
        result, self.extract = SendRequest(test_data.case_step_3, self.extract).send_request()

        report_setting(test_data.case_step_3)
        logger.info("*************** 结束执行用例 ***************\n")


if __name__ == '__main__':
    pytest.main(
        ["-q", "-s", "test_users_case.py", "-W", "ignore:Module already imported:pytest.PytestWarning"])
