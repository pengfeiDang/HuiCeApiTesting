import allure
import requests
import pytest
from allure_commons.types import LabelType

from apirunner.testcase import Step, RunRequest
from common.data_factory import telephone, RegisterUserData, LoginData


@allure.feature('会员管理模块')
@pytest.mark.MemberController
class TestAuthCode:

    @allure.story('正向验证获取验证码')
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_getAuthCode_001(self, runner):
        tel = telephone()
        res = requests.get(url=f'http://121.37.169.128:8201/mall-member/sso/getAuthCode?telephone={tel}')
        d: dict = res.json()
        assert d.get('code') == 200

    @pytest.mark.nagitave
    def test_getAuthCode_002(self):
        res = requests.get(url='http://121.37.169.128:8201/mall-member/sso/getAuthCode?telephone=134')
        d: dict = res.json()
        assert d.get('code') == 500

    @pytest.mark.nagitave
    def test_getAuthCode_003(self):
        res = requests.get(url='http://121.37.169.128:8201/mall-member/sso/getAuthCode?telephone=')
        d: dict = res.json()
        assert d.get('code') == 500


@pytest.mark.MemberController
class TestRegister:

    @pytest.mark.parametrize('data', RegisterUserData.userData(iterations=2))
    def test_RegisterUser(self, session, data):
        # 接口一：获取验证码
        tel = telephone()
        res = session.get(url=f'http://121.37.169.128:8201/mall-member/sso/getAuthCode?telephone={tel}')
        d: dict = res.json()
        code = d.get('data')

        # 接口二：提交注册（验证码数据来自于接口一）
        data['authCode'] = code
        data['telephone'] = tel
        res = session.post(url='http://121.37.169.128:8201/mall-member/sso/register', data=data)
        d = res.json()

        assert d.get('code') == 200
        assert d.get('message') == '注册成功'


@pytest.mark.MemberController
class TestLogin:
    @pytest.mark.parametrize("user", LoginData.loginData())  # 有两条数据
    def test_login_001(self, user):
        print(user.get('username'))
        print(user.get('password'))


@pytest.mark.MemberController
class TestMemberInfo:
    def test_get_memberInfo(self, session, token):
        headers = {'Authorization': token}
        res = session.get(url='http://121.37.169.128:8201/mall-member/sso/info', headers=headers)
        d: dict = res.json()
        assert d.get('code') == 200
        assert d.get('message') == '操作成功'


if __name__ == '__main__':
    pytest.main(['-s'])

# 1、生成唯一手机号
# 2、获取验证码（如果被很多用例使用，建议封装成一个通用的模块）
# 3、构造用户数据
# 4、请求和验证
# Junit  setup  测试方法1  tearDown   setup  测试方法2 tearDown
# fixture
