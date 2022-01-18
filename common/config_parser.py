# _*_ coding:utf-8 _*_
import configparser
import os


class Config:
    # 类变量
    __configfile = os.path.abspath(os.path.dirname(os.path.dirname(__file__)) + r"/common/config.ini")
    # __configfile = r'/Users/mac/PycharmProjects/HuiCeApiTesting/common/config.ini'

    # 方法或者函数的参数种类
    # 1、必选参数，参数名没有任何修饰，一定要定义在参数最前面
    # 2、可选参数
    #   1）默认值参数
    #   2）传元组或者列表（函数内自动转换成元组），定义方式：在参数名前加*
    #   3）传字典，定义方式：在参数名前加**

    # 类中所有方法的第一个参数，代表的是当前对象自身，名字可以随意起
    # 字典中的key是字符串类型，字典中的value可以是任意数据类型
    def __init__(self, *args):
        con = configparser.ConfigParser()
        con.read(Config.__configfile)
        self.__testcase_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + con.get('testcase', 'path')
        self.__result_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + con.get('report', 'result_path')
        self.__report_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + con.get('report', 'report_path')

    @property
    def testcase_path(self):
        return self.__testcase_path

    @property
    def result_path(self):
        return self.__result_path

    @property
    def report_path(self):
        return self.__report_path


config = Config()  # 单例设计
# print(config.testcase_path)

# import os
# path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)) + r"/common/config.ini")
# print(path)

