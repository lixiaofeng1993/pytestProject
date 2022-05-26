import os
import pytest
from pytest_jsonreport.plugin import JSONReport
from public.send_ding import send_ding

if __name__ == '__main__':
    plugin = JSONReport()
    pytest.main(plugins=[plugin])
    send_ding(plugin)
    os.system("allure generate ./report --clean allure-reports -o ./report/html")
