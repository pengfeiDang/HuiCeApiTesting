import allure
import pytest

from apirunner.models import Severity
from apirunner.runner import APIRunner
from apirunner.testcase import Step, RunRequest, Config


@pytest.mark.fecmall
def test_index(runner):
    # 1、创建一个Step对象
    # 2、将该Step对象放入steps列表中
    runner.config = Config('首页').base_url('http://appserver.huice.com')

    runner.steps = [Step(
        RunRequest('获取首页信息')
            .get('/cms/home/index')
            .validate()
            .assert_equal('body.code', 200)
            .assert_equal('body.message', 'process success')
    ), ]
    runner.run()


@pytest.mark.fecmall
def test_customer_login(runner):
    runner.config = Config('登录').base_url('http://appserver.huice.com/customer') \
        .with_feature('fecmall购物系统') \
        .with_story('用户管理模块') \
        .with_severity(Severity.CRITICAL)

    runner.steps = [Step(
        RunRequest('登录')
            .post('/login/account')
            .with_data({'email': '65132090@qq.com', 'password': '123456'})
            .validate()
            .assert_equal('body.code', 200)
            .assert_equal('body.message', 'process success')
    ), ]
    runner.run()


@pytest.mark.fecmall99
def test_customer_address(runner):
    runner.config = Config('登录').base_url('http://appserver.huice.com')  # 登录--用例名称

    runner.steps = [
        Step(
            RunRequest('登录')  # 执行步骤名称
                .post('/customer/login/account')
                .with_data({'email': '65132090@qq.com', 'password': '123456'})
                .extract()
                .with_jmespath('headers."Access-Token"', 'token')
        ),
        # access_token('65132090@qq.com', '123456', runner.session)
        Step(
            RunRequest('获取地址列表')
                .get('/customer/address/index')
                .with_headers(**{'access-token': '$token'})
                .validate()
                .assert_equal('body.code', 200)
                .assert_equal('body.message', 'process success')
        ), ]
    runner.run()

# if __name__ == '__main__':
#     runner = APIRunner()
#     runner.config = Config('登录').base_url('http://appserver.huice.com')
#
#     runner.steps = [
#         Step(
#             RunRequest('登录')
#                 .post('/login/account')
#                 .with_data({'email': '65132090@qq.com', 'password': '123456'})
#                 .extract()
#                 .with_jmespath('headers.Access-Token', 'token')
#         ),
#         # access_token('65132090@qq.com', '123456', runner.session)
#         Step(
#             RunRequest('获取地址列表')
#                 .get('/customer/address/index')
#                 .with_headers(**{'access-token': '$token'})
#                 .validate()
#                 .assert_equal('body.code', 200)
#                 .assert_equal('body.message', 'process success')
#         ), ]
#     runner.run()
