from typing import Dict, Text, Any

import jmespath
import requests
from jmespath.exceptions import JMESPathError
from loguru import logger

from apirunner.models import Validators
from apirunner import loader


def get_uniform_comparator(comparator: Text):
    """ convert comparator alias to uniform name
    """
    if comparator in ["eq", "equals", "equal"]:
        return "equal"
    elif comparator in ["lt", "less_than"]:
        return "less_than"
    elif comparator in ["le", "less_or_equals"]:
        return "less_or_equals"
    elif comparator in ["gt", "greater_than"]:
        return "greater_than"
    elif comparator in ["ge", "greater_or_equals"]:
        return "greater_or_equals"
    elif comparator in ["ne", "not_equal"]:
        return "not_equal"
    elif comparator in ["len_eq", "length_equal"]:
        return "length_equal"
    elif comparator in [
        "len_gt",
        "length_greater_than",
    ]:
        return "length_greater_than"
    elif comparator in [
        "len_ge",
        "length_greater_or_equals",
    ]:
        return "length_greater_or_equals"
    elif comparator in ["len_lt", "length_less_than"]:
        return "length_less_than"
    elif comparator in [
        "len_le",
        "length_less_or_equals",
    ]:
        return "length_less_or_equals"
    else:
        return comparator


def uniform_validator(validator: Dict):
    """
    对断言信息做统一处理
    :param validator:
    :return:
    """
    # 取出断言函数名
    comparator = list(validator.keys())[0]
    # 取出断言的三个参数
    compare_values = validator[comparator]
    check_item = compare_values[0]
    expect_value = compare_values[1]
    if len(compare_values) == 3:
        message = compare_values[2]
    else:
        message = ""
    # 统一断言函数名，例如： lt => less_than, eq => equals
    assert_method = get_uniform_comparator(comparator)
    return {
        "check": check_item,
        "expect": expect_value,
        "assert": assert_method,
        "message": message,
    }


class ResponseObject:
    def __init__(self, resp_obj: requests.Response):
        """ initialize with a requests.Response object
        Args:
            resp_obj (instance): requests.Response instance
        """
        self.resp_obj = resp_obj

    def __getattr__(self, key):
        if key in ["json", "content", "body"]:
            try:
                value = self.resp_obj.json()
            except ValueError:
                value = self.resp_obj.content
        elif key == "cookies":
            value = self.resp_obj.cookies.get_dict()
        else:
            try:
                value = getattr(self.resp_obj, key)
            except AttributeError:
                err_msg = "ResponseObject does not have attribute: {}".format(key)
                logger.error(err_msg)

        self.__dict__[key] = value
        return value

    def __search_jmespath(self, expr: Text) -> Any:
        # 设置检索范围
        resp_obj_meta = {
            "status_code": self.status_code,
            "headers": self.headers,
            "cookies": self.cookies,
            "body": self.body,
        }
        try:
            check_value = jmespath.search(expr, resp_obj_meta)#通过key查询value
        except JMESPathError as ex:
            logger.error(
                f"failed to search with jmespath\n"
                f"expression: {expr}\n"
                f"data: {resp_obj_meta}\n"
                f"exception: {ex}"
            )
            check_value = None

        return check_value

    def extract(self, extractors: Dict[Text, Text]) -> Dict[Text, Any]:
        if not extractors:
            return {}

        extract_mapping = {}
        for key, field in extractors.items():
            field_value = self.__search_jmespath(field)
            extract_mapping[key] = field_value

        logger.info(f"extract mapping: {extract_mapping}")
        return extract_mapping

    def validate(self, validators: Validators):
        # 加载所有断言函数
        functions_mapping = loader.load_comparator_functions()
        for v in validators:
            # 对断言信息二次加工处理
            u_validator = uniform_validator(v)
            assert_method = u_validator.get('assert')
            assert_func = functions_mapping.get(assert_method)
            expect_value = u_validator.get('expect')
            message = u_validator.get('message')
            check_item = u_validator.get('check')
            # 从返回的数据中获取指定的检查内容
            check_value = self.__search_jmespath(check_item)

            assert_func(check_value, expect_value, message)
