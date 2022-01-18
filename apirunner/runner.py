import os
from typing import List, Text, Union

import requests
from apirunner.models import TStep, TConfig, VariablesMapping, StepData
from apirunner.parser import parse_data
from apirunner.response import ResponseObject
from apirunner.testcase import Step, Config
from apirunner.loader import load_testcase_file
from apirunner.utils import merge_variables, report_allure


class APIRunner:
    # 保存需要运行的测试步骤（提供的用户使用接口）

    # 真正执行的数据
    # __tSteps: List[TStep]

    def __init__(self):
        self.__session = requests.session()

        self.steps: List[Step] = []
        self.__tSteps: List[TStep] = []
        self.config = Config('测试配置')
        self.__tConfig: Union[TConfig, None] = None

    def __init_tests(self):
        self.__tSteps = []
        self.__tConfig = self.config.perform()
        for step in self.steps:
            self.__tSteps.append(step.perform())

    def __run_step(self):
        extracted_variables: VariablesMapping = {}
        report_allure(config=self.__tConfig)
        for step in self.__tSteps:
            # override variables
            # step variables > extracted variables from previous steps
            report_allure(step=step)
            step.variables = merge_variables(step.variables, extracted_variables)
            # step variables > testcase config variables
            step.variables = merge_variables(step.variables, self.__tConfig.variables)

            step_data = StepData(name=step.name)

            request_dict = step.request.dict()
            parsed_request_dict = parse_data(
                request_dict, step.variables
            )
            step.variables["request"] = parsed_request_dict

            # 将key为req_json字典替换成key为json的字典
            parsed_request_dict['json'] = parsed_request_dict.pop('req_json', {})
            url = self.__tConfig.base_url + parsed_request_dict.pop("url")

            res = self.__session.request(url=url, method=parsed_request_dict.pop("method"), **parsed_request_dict)
            res_obj = ResponseObject(res)
            step.variables["response"] = res_obj

            # extract
            extractors = step.extract
            extract_mapping = res_obj.extract(extractors)
            step_data.export_vars = extract_mapping

            variables_mapping = step.variables
            variables_mapping.update(extract_mapping)

            # validate
            res_obj.validate(step.validators)

            extracted_variables.update(extract_mapping)

    def run_path(self, path: Text):
        """
        基于解析yml文件的方式填充每个测试步骤数据
        :param path:
        :return:
        """
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Invalid testcase path: {path}")
        testcase = load_testcase_file(path)
        self.__tSteps = testcase.steps
        self.__tConfig = testcase.config

        self.__run_step()

    def run(self):
        """
        基于自行写代码的方式填充每个测试步骤数据
        :return:
        """
        self.__init_tests()
        self.__run_step()

    @property
    def session(self):
        return self.__session

    def close(self):
        self.__session.close()


# if __name__ == '__main__':
#     r = APIRunner()
#     r.run_path(
#         r'/Users/mac/PycharmProjects/HuiCeApiTesting/testcase_yaml_files/fecmall/test_get_address.yml')
# 服务器端返回的数据 response = '{"code":200,"message":"获取验证码成功","data":"558642"}'，
# v = {'contains': ['message', '成功', '验证提示信息']}
# check_value = response.json().get(v.get('contains')[0]) # 来自于接口返回的数据
# expect_value = v.get('contains')[1]    # 来自于你的断言
# 从response对象中获取断言中需要验证的数据，
# 例如返回的数据：'{"code":200,"message":"获取验证码成功","data":"558642"}'，
# 假设断言信息：v = {'contains': ['message', ’成功‘, '验证提示信息']}
# 根据断言取出返回数据的code的值：保存到check_value=200
# 根据断言取出期望的值：保存到expect_value=200
# 根据断言的key信息，执行相应的断言：equal(check_value, expect_value)
#
#
# class TestCase1(APIRunner):
#
#     def test1(self):
#         self.steps = [
#             Step(
#                 RunRequest('获取验证码')
#                     .get('http://121.37.169.128:8201/mall-member/sso/getAuthCode')
#                     .with_params(**{'telephone': '1340182883'})
#                     .validate()
#                     .assert_contains('body.message', '成功88', '验证提示信息')
#                     .assert_equal('body.code', 2000, '验证状态码')
#             ),
#             # Step(
#             #     RunRequest('获取验证码')
#             #         .get('http://121.37.169.128:8201/mall-member/sso/getAuthCode')
#             #         .with_params(**{'telephone': '1340182883'})
#             # )
#         ]
#         self.run()
#
#
# TestCase1().test1()
# # 将请求对象转换成字典
#           step_dict = step.request.dict()
#           # 将key为req_json字典替换成key为json的字典
#           step_dict['json'] = step_dict.pop('req_json', {})
#           response = self.__session.request(url=step_dict.pop("url"), method=step_dict.pop("method"), **step_dict)
#           res_obj = ResponseObject(response)
# def hello(m1, m2, m3):
#     print('慧测欢迎您')
#
#
# # Callable:可以被调用的函数或者方法
# def test1(name: Callable):
#     # 函数调用
#     name(1, 2, 3)
#
#
# # - equal: ["code", 200, '验证状态码']
# # - equal: ["message", "获取验证码成功", '验证提示信息']
#
# test1(hello)
# # code的值会从实际返回的结果中提取出来的,这里假设值已经取到，是200
# v1 = {'equal': [200, 200, '验证状态码']}
# v2 = {'contains': ['获取验证码成功', '获取验证码成功88', '验证提示信息']}
#
# # for k,v in v1.items():
# #     k(v[0],v[1],v[2])
# from common import loader
#
# validators = []
# validators.append(v1)
# validators.append(v2)
# m = loader.load_comparator_functions()
#
# for items in validators:
#     for k, v in items.items():
#         m.get(k)(v[0], v[1], v[2])
#         # k(v[0], v[1], v[2])
#
# #
# from common.comparator import *
# if __name__ == '__main__':
#     res = requests.get(url='http://121.37.169.128:8201/mall-member/sso/getAuthCode?telephone=13401182883')
#     data: Dict = res.json()
#     # 断言 == <=  <  > >=
#
#     assert len(data.get('data')) == 6
#
#     rule = '获取' + r'(.+?)' + '成功'
#     regex_match(data.get('message'),rule)
#
#     assert  str(data.get('message')).startswith('获取')
# assert 20000 == data.get('code'),'验证状态码'
# assert 200 <= data.get('code')
#
# assert '获取验证码成功' == data.get('message')
# assert '成功' in data.get('message')

# assert 表达式
