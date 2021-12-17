# pytestProject

## [点击这里](https://www.cnblogs.com/changqing8023/p/15608857.html)


## 环境

* python版本3.6
    * 必须安装的python包：
        ```yaml
        Faker==1.0.5
        jsonpath==0.82
        markdown2==2.3.8
        PyMySQL==0.9.3
        cx_Oracle==8.3.0
        pytest==5.4.3
        PyYAML==5.1.2
        requests==2.22.0
        requests_toolbelt==0.9.1
        allure-pytest==2.9.45
        ```
* allure工具安装
    * 项目目录 tools/allure-2.13.6.rar 文件，解压并配置 bin 目录环境变量即可

## 新增用例步骤

* 在 testcase/ 目录下新建对应页面的目录
    * eg：baseInfo/
* 在 baseInfo/ 目录下新建页面 continentInfo/ 大洲信息 页面目录
* 在 continentInfo/ 目录下新建 data/ 目录 和 接口测试用例 py 文件
    * data/ 目录下包含
        * data.yml 文件
            * **命名是唯一的，continentInfo/ 目录下可以多个测试用例 py 文件对应一个 data.yml**
            * **测试用例 py 文件中的 方法名称，在 data.yml 中必须有对应的一级目录<最外层命名>**
            * data.yml 格式可以参考 tools/ 目录下
                * 上下文依赖的非参数化接口.yml
                * 单个接口yml文件参数化.yml
                * 有依赖的单个接口参数化.yml
        * 参数化 csv 文件
        * 上传接口 上传的文件
        * 下载文件接口 下载的文件
    * 接口测试用例 py 文件 格式基本固定
    ```python
    
    import pytest
    from public.send_request import SendRequest  # 处理http请求
    from public.log import logger  # 日志
    from public.sql_to_data import SqlToData  # 处理测试用例数据
    from public.help import get_data_path, os, fun_name, report_setting, report_step_setting, allure
    
    data_path = get_data_path(os.path.dirname(__file__))  # 返回当前文件的绝对路径
    test_params = SqlToData().yaml_db_query(data_path)  # 返回处理后的测试数据
    
    
    @allure.severity(allure.severity_level.TRIVIAL)  # 测试类等级
    @allure.epic(test_params.get("epic"))  # allure报告一级目录
    @allure.feature(test_params.get("feature"))  # allure报告二级目录
    class TestContinentInfo:  # 测试类
    
        def setup_class(self):
            self.extract = {}  # 全局变量
        
        # 参数化
        @pytest.mark.parametrize("data", test_params["test_page_query_case"].parametrize)  # pytest参数化装饰器
        def test_page_query_case(self, data):
            logger.info("*************** 开始执行用例 ***************")
            # 获取执行用例函数名
            name = fun_name()
            # 报告展示的测试步骤
            report_step_setting(test_params[name])
    
            # 重置测试数据
            test_params[name].parametrize = data
            # 发送接口请求，断言，返回提取变量字典
            self.extract = SendRequest(test_params[name], self.extract).send_request()
    
            # 报告上展示的测试标题等
            report_setting(test_params[name])
            logger.info("*************** 结束执行用例 ***************\n")

        
        # 非参数化 依赖的 conftest.py 参考 tools/conftest.py
        def test_page_add_case(self, test_data):
            logger.info("*************** 开始执行用例 ***************")
            # 报告展示的测试步骤
            report_step_setting(test_data)
    
            # 依赖接口，返回依赖数据
            result, self.extract = SendRequest(test_data.case_step_1, self.extract).send_request()
            
            # 替换依赖数据
            result, self.extract = SendRequest(test_data.case_step_2, self.extract).send_request()
    
            # 报告上展示的测试标题等
            report_setting(test_data)
            logger.info("*************** 结束执行用例 ***************\n")
        ```

## 测试数据

* `test_params = SqlToData().yaml_db_query(data_path)` 中 test_params 被封装成了一个 `ObjectData` 对象
* `ObjectData` 对象 会动态的加载 data.yml 中设置的属性和值
* `配置文件` 中可以设置 `用例依赖接口数量`，这个数值是依赖接口的最大数量
    * 这里的依赖接口命名 必须是 **case_step_{i}** 
    * i 值：0，1，2，3，4，5 ... 等

## 断言

* 支持如下断言
    * equal 相等
    * not_equal 不相等
    * contains 包含
    * notcontains 不包含
    * startswith 以xx开始
    * endswith 以xx结束
    * greater_than 实际值大于期望值
    * less_than 实际值小于期望值
    * greater_or_equals 实际值大于等于期望值
    * less_or_equals 实际值小于等于期望值
    * regex_match 正则匹配
