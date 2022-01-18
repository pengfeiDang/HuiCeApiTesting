import csv
import json
import os
import types

import yaml
from typing import Text, Dict, List, Callable
from loguru import logger
from pydantic import ValidationError
from apirunner.models import TestCase
from apirunner.builtin import comparator


def load_comparator_functions() -> Dict[Text, Callable]:
    """
    加载断言函数
    :return:
    """
    module_functions = {}
    for name, item in vars(comparator).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item
    return module_functions


def load_yaml_file(yaml_file: Text) -> Dict:
    with open(yaml_file, mode='rb') as fp:
        try:
            yaml_content = yaml.load(fp, yaml.Loader)
        except yaml.YAMLError as e:
            logger.error(e)
        return yaml_content


def load_json_file(json_file: Text) -> Dict:
    with open(json_file, mode='rb') as fp:
        try:
            json_content = json.load(fp)
        except json.JSONDecodeError as e:
            logger.error(e.msg)
        return json_content


def load_csv_file(csv_file: Text) -> List[Dict]:
    """
    Examples:
    # >>> cat csv_file
    username,email,password
    huice001,65132090@qq.com,pwd001
    huice002,123456@qq.com,pwd002
    # >>> load_csv_file(csv_file)
    [
        {'username':'huice001','email':'65132090@qq.com','password':'pwd001'},
        {'username':'huice002','email':'123456@qq.com','password':'pwd002'}
    ]
    :param csv_file:
    :return:
    """
    # try  exception

    csv_content_list = []
    with open(csv_file, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_content_list.append(row)

    return csv_content_list


def load_test_file(test_file: Text) -> Dict:
    """load testcase/testsuite file content"""
    if not os.path.isfile(test_file):
        raise FileNotFoundError(f"test file not exists: {test_file}")

    file_suffix = os.path.splitext(test_file)[1].lower()
    if file_suffix == ".json":
        test_file_content = load_json_file(test_file)
    elif file_suffix in [".yaml", ".yml"]:
        test_file_content = load_yaml_file(test_file)
    else:
        # '' or other suffix
        logger.error(f"testcase/testsuite file should be YAML/JSON format, invalid format file: {test_file}")

    return test_file_content


def load_testcase(testcase: Dict) -> TestCase:
    try:
        # validate with pydantic TestCase model
        testcase_obj = TestCase.parse_obj(testcase)
    except ValidationError as ex:
        err_msg = f"TestCase ValidationError:\nerror: {ex}\ncontent: {testcase}"
        logger.error(err_msg)

    return testcase_obj


def load_testcase_file(testcase_file: Text) -> TestCase:
    """load testcase file and validate with pydantic model"""
    # 通过yaml加载模块，加载整个yml数据到testcase_content对象

    testcase_content = load_test_file(testcase_file)
    print(testcase_content)
    testcase_obj = load_testcase(testcase_content)
    return testcase_obj


if __name__ == '__main__':
    f = load_testcase_file(r'/Users/mac/PycharmProjects/HuiCeApiTesting/testcase_yaml_files/fecmall/test_index.yml')
    print(f)