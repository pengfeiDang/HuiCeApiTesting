import os

import pytest
import requests
from apirunner.runner import APIRunner
from common.config_parser import config


# @pytest.fixture(scope='session', autouse=True)
# def report():
#     print('开始生成测试报告......')
#     yield
#     # os.system(f'rd /s/q {config.report_path}')#每次手动删除report目录里的内容，刷新报告
#     # os.system(fr'rm -rf {config.report_path}/*')#每次手动删除report目录里的内容，刷新报告
#     os.popen(
#         r'allure generate ' +
#         config.result_path + ' -o ' +
#         config.report_path)
#     # os.popen(cmd=fr'allure generate {config.result_path} -o {config.report_path}')
#
#     os.system(fr'allure open {config.report_path}')#测试完成打开报告
#     # os.system(fr'allure serve {config.result_path}')
#     print('测试报告生成完成......')


@pytest.fixture()
def session():
    s = requests.session()
    yield s
    s.close()


@pytest.fixture()
def runner():
    r = APIRunner()
    yield r
    r.close()


@pytest.fixture()
def token(session):
    data = {'username': 'huice999', 'password': '123456'}
    res = session.post(url='http://121.37.169.128:8201/mall-member/sso/login', data=data)
    d: dict = res.json()
    return d.get('data').get('tokenHead') + d.get('data').get('token')
