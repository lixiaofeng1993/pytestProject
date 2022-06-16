#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: test_project_case.py
# 说   明: 
# 创建时间: 2022/5/29 10:22
# @Version：V 0.1
# @desc :
import pytest
from public.send_request import SendRequest
from public.log import logger
from public.sql_to_data import SqlToData
from public.help import get_data_path, get_project_name, os, fun_name, report_setting, report_step_setting, allure

case_path = os.path.dirname(__file__)
project_name = get_project_name(case_path)
data_path = get_data_path(case_path)
test_params = SqlToData().yaml_db_query(data_path)


@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic(test_params.get("epic"))
@allure.feature(test_params.get("feature"))
class TestProjectCase:

    def setup_class(self):
        self.extract = {"project_name": project_name}

    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("data", test_params["test_create_project_case"].parametrize)
    def test_create_project_case(self, data, test_data):  # TODO: 使用 test_params[name] jinja2 无法替换yml文件中的token()函数
        logger.info("*************** 开始执行用例 ***************")
        # 报告展示的测试步骤
        report_step_setting(test_data.case_step_1)
        result, self.extract = SendRequest(test_data.case_step_1, self.extract).send_request()

        # 报告展示的测试步骤
        report_step_setting(test_data)
        # 重置测试数据
        test_data.parametrize = data
        # 发送接口请求，断言，返回提取变量字典
        result, self.extract = SendRequest(test_data, self.extract).send_request()

        # 报告上展示的测试标题等
        report_setting(test_data)
        logger.info("*************** 结束执行用例 ***************\n")


if __name__ == '__main__':
    pytest.main(
        ["-q", "-s", "test_project_case.py", "-W", "ignore:Module already imported:pytest.PytestWarning"])
