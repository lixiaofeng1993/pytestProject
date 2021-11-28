import os
import pytest

if __name__ == '__main__':
    pytest.main()
    os.system("allure generate ./report --clean allure-reports -o ./report/html")
    # import httprunner