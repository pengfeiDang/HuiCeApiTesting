# from apirunner.runner import APIRunner
# from apirunner.testcase import Step, Config, RunRequest
#
# if __name__ == '__main__':
#     runner = APIRunner()
#     runner.config = Config('登录').base_url('http://appserver.huice.com')
#
#     runner.steps = [
#         Step(
#             RunRequest('登录')
#                 .post('/customer/login/account')
#                 .with_data({'email': '65132090@qq.com', 'password': '123456'})
#                 .extract()
#                 .with_jmespath('headers."Access-Token"', 'token')
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
#
#
# # import os
# #
# # import requests
# #
# # from apirunner.runner import APIRunner
# # from apirunner.testcase import RunRequest
# # from common import tools
# #
# # base_url = "http://bbs.huice.com"
# # # session = requests.session()
# # api = APIRunner()
# # # ---------------------------------------------步骤一------------------------------------------
# # data = {'fastloginfield': 'username',
# #         'username': 'huice0008',
# #         'password': 'huice0008',
# #         'quickforward': 'yes',
# #         'handlekey': 'ls'
# #         }
# # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# # params = {'mod': 'logging', 'action': 'login', 'loginsubmit': 'yes', 'infloat': 'yes', 'lssubmit': 'yes', 'inajax': '1'}
# # req = RunRequest('步骤一：登录')
# # # 获取TStep对象
# # step = req.post(base_url + '/member.php').with_params(**params).with_data(data).with_headers(**headers).perform()
# # # 将请求对象转换成字典
# # # step_dict = step.request.dict()
# # # # 将key为req_json字典替换成key为json的字典
# # # step_dict['json'] = step_dict.pop('req_json', {})
# # #
# # # response = session.request(url=step_dict.pop("url"), method=step_dict.pop("method"), **step_dict)
# # # print(response.text)
# #
# # # # --------------------------------------步骤二：点击发帖，获取服务器端返回的hash和uid等关键数据------------------
# # #
# # # req = RunRequest('步骤二：点击发帖')
# # # params = {'mod': 'forumdisplay', 'fid': 36}
# # # step = req.get(base_url + '/forum.php').with_params(**params).perform()
# # # response = api.run_step(step)
# # # 将请求对象转换成字典
# # # step_dict = step.request.dict()
# # # # 将key为req_json字典替换成key为json的字典
# # # step_dict['json'] = step_dict.pop('req_json', {})
# # #
# # # response = session.request(url=step_dict.pop("url"), method=step_dict.pop("method"), **step_dict)
# # # print(response.text)
# #
# # # 获取该请求返回的uid和hash、formhash
# # uid = tools.find_all_data(response.text, LB='uid=', RB='"')[0]
# # hash = tools.find_all_data(response.text, LB='"hash":"', RB='"')[0]
# # formhash = tools.find_all_data(response.text, LB='"formhash" value="', RB='"')
# #
# #
# # # --------------------------------步骤三：上传附件----------------------------------------
# # req = RunRequest('上传附件')
# # params = {'mod': 'swfupload', 'action': 'swfupload', 'operation': 'upload', 'fid': 36}
# # filename = r'C:\Users\86134\Desktop\software\BAK\locust.jpg'
# # file_size = os.path.getsize(filename)
# # with open(filename, 'rb') as fp:
# #     files = {'Filedata': fp}
# #     data = {'uid': uid, 'type': 'image/jpeg', 'size': file_size, 'hash': hash, 'filetype': 'image/jpeg'}
# #     step = req.post(base_url + "/misc.php").with_data(data).with_params(**params).with_files(
# #         **files).perform()
# #     # 将请求对象转换成字典
# #     response = api.run_step(step)
# #     # step_dict = step.request.dict()
# #     # # 将key为req_json字典替换成key为json的字典
# #     # step_dict['json'] = step_dict.pop('req_json', {})
# #     #
# #     # response = session.request(url=step_dict.pop("url"), method=step_dict.pop("method"), **step_dict)
# #     # print(response.text)
# #
# # # -------------------------------步骤四：提交帖子---------------------------------------
# # params = {'mod': 'post', 'action': 'newthread', 'fid': 36, 'extra': '', 'topicsubmit': 'yes'}
# # file_desc = 'attachnew[' + response.text + '][description]'
# # data = {
# #     'subject': '慧测自动化测试666666666666',
# #     'posttime': '1636358243',
# #     'message': '慧测自动化哈哈开课了',
# #     'formhash': formhash,
# #     'file': '',
# #     f'attachnew[{response.text}][description]': '123附件描述testing',
# #     'usesig': 1
# # }
# #
# # req = RunRequest('提交帖子')
# # step = req.post(base_url + '/forum.php').with_params(**params).with_data(data).perform()
# #
# #
# # response = api.run_step(step)
# # # 将请求对象转换成字典
# # # step_dict = step.request.dict()
# # # # 将key为req_json字典替换成key为json的字典
# # # step_dict['json'] = step_dict.pop('req_json', {})
# # #
# # # response = session.request(url=step_dict.pop("url"), method=step_dict.pop("method"), **step_dict)
# # print(response.text)
#
#
# from mimesis import Person, Text, Schema, Internet
# from mimesis.enums import Locale
#
# p = Person(Locale.EN)
# i = Internet()
#
#
# def getdata():
#     data = {
#         "id": 0,
#         "category": {
#             "id": 0,
#             "name": p.name()
#         },
#         "name": p.username(),
#         "photoUrls": [
#             i.url()
#         ],
#         "tags": [
#             {
#                 "id": 0,
#                 "name": p.gender()
#             }
#         ],
#         "status": "available"
#     }
#     return data
#
# schema = Schema(schema=getdata)
# list1 = schema.create(iterations=3)
# print(list1)


import pytest
from common.config_parser import config


# pytest.main(['-s',  '-m', 'fecmall99', '--clean-alluredir', f'--alluredir={config.result_path}'])
pytest.main(['-s',  '-m', 'fecmall99', '--clean-alluredir', f'--alluredir=/Users/mac/jenkins/workspace/allure-results'])