from enum import Enum
from typing import Text, Dict, Union, Any, List

import allure
from pydantic import BaseModel, Field

# 定义数据类型别名
Validators = List[Dict]
VariablesMapping = Dict[Text, Any]


class RequestMethod(Text, Enum):
    """
    封装常见的请求方法
    """
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PUT = 'PUT'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'
    HEAD = 'HEAD'


class Severity(str, Enum):
    BLOCKER = 'blocker'
    CRITICAL = 'critical'
    NORMAL = 'normal'
    MINOR = 'minor'
    TRIVIAL = 'trivial'


class TRequest(BaseModel):
    """
    封装请求数据
    """
    method: RequestMethod
    url: Text
    params: Dict[Text, Text] = {}
    data: Union[Text, Dict[Text, Any]] = None
    req_json: Union[Dict, List, Text] = Field(None, alias="json")
    headers: Dict[Text, Text] = {}
    cookies: Dict[Text, Text] = {}
    files: Dict = {}
    timeout: float = 120
    allow_redirects: bool = True
    verify: bool = False


class TStep(BaseModel):
    """
    封装测试步骤信息
    """
    # 测试步骤名称
    name: Text
    # 请求对象（存储需要请求的参数信息）
    request: Union[TRequest, None] = None
    # 存储需要导出的返回数据信息，解决接口间的数据依赖
    extract: Dict[Text, Any] = {}
    variables: VariablesMapping = {}
    # 存储当前步骤的断言信息
    validators: Validators = Field([], alias="validate")


class TConfig(BaseModel):
    name: Text
    base_url: Text = ''
    variables: VariablesMapping = {}
    feature: Text = ''
    story: Text = ''
    severity: Severity = Severity.NORMAL


class TestCase(BaseModel):
    config: TConfig
    steps: List[TStep]


class StepData(BaseModel):
    """teststep data, each step maybe corresponding to one request or one testcase"""
    success: bool = False
    name: Text = ""  # teststep name
    export_vars: VariablesMapping = {}
