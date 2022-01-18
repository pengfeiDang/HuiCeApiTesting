import requests

from common.data_factory import telephone, RegisterUserData


def token(username, password, session=None):
    if session is None:
        session = requests.session()
    data = {'username': username, 'password': password}
    res = session.post(url='http://121.37.169.128:8201/mall-member/sso/login', data=data)
    d: dict = res.json()
    return d.get('data').get('tokenHead') + d.get('data').get('token')


def registerUser(session=None):
    # 接口一：获取验证码
    tel = telephone()
    res = session.get(url=f'http://121.37.169.128:8201/mall-member/sso/getAuthCode?telephone={tel}')
    d: dict = res.json()
    code = d.get('data')

    data = RegisterUserData.userData()[0]
    # 接口二：提交注册（验证码数据来自于接口一）
    data['authCode'] = code
    data['telephone'] = tel
    res = session.post(url='http://121.37.169.128:8201/mall-member/sso/register', data=data)
    return data.get('username'), data.get('password')


def access_token(email, password, session=None):
    if session is None:
        session = requests.session()
    res = session.post(url='http://appserver.huice.com/customer/login/account',
                       data={'email': email, 'password': password})
    return res.headers.get('Access-Token')
