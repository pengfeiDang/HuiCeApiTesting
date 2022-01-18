from common.common_interface import token, registerUser
import pytest


@pytest.mark.UmsMemberReceiveAddressController
class TestAddReceiveAddress:

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_add_receive_address_001(self, session):
        data = {
            "city": "北京",
            "defaultStatus": 0,
            "detailAddress": "北京朝阳区汤立路220号院",
            "id": 0,
            "memberId": 0,
            "name": "公司地址",
            "phoneNumber": "13401182883",
            "postCode": "",
            "province": "北京",
            "region": "华北"
        }
        # 接口一  注册新用户并返回用户名和密码
        username, password = registerUser(session=session)
        # 接口二  登录
        newtoken = token(username, password, session=session)
        # 接口三
        headers = {'Content-Type': 'application/json', 'Authorization': newtoken}
        res = session.post(url='http://121.37.169.128:8201/mall-member/member/address/add', json=data, headers=headers)
        d = res.json()
        assert d.get('code') == 200
