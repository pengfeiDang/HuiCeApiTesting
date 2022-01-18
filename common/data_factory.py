import os
import random
from mimesis import Person, Schema
from common.config_parser import config


def telephone():
    # 所有的头信息添加上来
    phon = [133, 149, 153, 173, 177, 180, 181, 189, 191, 199, 130, 131, 132, 145, 155, 156, 166, 171, 175, 176, 185,
            186, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 172, 178, 182, 183, 184, 187, 188, 198]
    phone = str(random.choice(phon)) + "".join(random.choice("0123456789") for i in range(8))
    return phone


class RegisterUserData:
    @staticmethod
    def userData(iterations=1):
        p = Person()
        schema = Schema(schema=lambda: {
            'authCode': '$authCode',
            'username': p.username(),
            'password': '123456',
            'telephone': '$tel'
        })
        return schema.create(iterations=iterations)


class TestCaseYamlFile:
    @staticmethod
    def yamlFiles():
        for rootDir, Temps, files in os.walk(config.testcase_path):
            return [rootDir + '\\' + file for file in files]


class LoginData:
    @staticmethod
    def loginData():
        return [{'username': 'huice001', 'password': '123456'}, {'username': 'huice002', 'password': '123456'}]


if __name__ == '__main__':
    for root, dirs, files in os.walk(
            r'C:\Users\86134\Documents\BaiduNetdiskWorkspace\workspace\HCTesting\testcase_yaml_files\fecmall'):
        print(root)
        print(files)
        print([root + '\\' + file for file in files])
    # s = RegisterUserData.userData()
    # print(s)
