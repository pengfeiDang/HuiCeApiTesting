from typing import Text, Any, Union

from apirunner.models import TRequest, RequestMethod, TStep, TConfig, Severity


class Config(object):
    def __init__(self, name: Text):
        self.__name = name
        self.__variables = {}
        self.__base_url = ""
        self.__feature = ''
        self.__story = ''
        self.__severity = Severity.NORMAL

    def with_feature(self, feature):
        self.__feature = feature
        return self

    def with_story(self, story):
        self.__story = story
        return self

    def with_severity(self, severity):
        self.__severity = severity
        return self

    def variables(self, **variables) -> "Config":
        self.__variables.update(variables)
        return self

    def base_url(self, base_url: Text) -> "Config":
        self.__base_url = base_url
        return self

    def perform(self) -> TConfig:
        return TConfig(
            name=self.__name,
            base_url=self.__base_url,
            variables=self.__variables,
            feature=self.__feature,
            story=self.__story,
            severity=self.__severity
        )


class StepRequestValidation:
    """
    将用户的断言信息填充到TStep中的validators对象
    """

    def __init__(self, step_context: TStep):
        self.__step_context = step_context

    def assert_equal(
            self, jmespath: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"equal": [jmespath, expected_value, message]}
        )
        return self

    def assert_not_equal(
            self, jmespath: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"not_equal": [jmespath, expected_value, message]}
        )
        return self

    def assert_greater_than(
            self, jmespath: Text, expected_value: Union[int, float], message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"greater_than": [jmespath, expected_value, message]}
        )
        return self

    def assert_less_than(
            self, jmespath: Text, expected_value: Union[int, float], message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"less_than": [jmespath, expected_value, message]}
        )
        return self

    def assert_greater_or_equals(
            self, jmespath: Text, expected_value: Union[int, float], message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"greater_or_equals": [jmespath, expected_value, message]}
        )
        return self

    def assert_less_or_equals(
            self, jmespath: Text, expected_value: Union[int, float], message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"less_or_equals": [jmespath, expected_value, message]}
        )
        return self

    def assert_length_equal(
            self, jmespath: Text, expected_value: int, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"length_equal": [jmespath, expected_value, message]}
        )
        return self

    def assert_length_greater_than(
            self, jmespath: Text, expected_value: int, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"length_greater_than": [jmespath, expected_value, message]}
        )
        return self

    def assert_length_less_than(
            self, jmespath: Text, expected_value: int, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"length_less_than": [jmespath, expected_value, message]}
        )
        return self

    def assert_length_greater_or_equals(
            self, jmespath: Text, expected_value: int, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"length_greater_or_equals": [jmespath, expected_value, message]}
        )
        return self

    def assert_length_less_or_equals(
            self, jmespath: Text, expected_value: int, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"length_less_or_equals": [jmespath, expected_value, message]}
        )
        return self

    def assert_startswith(
            self, jmespath: Text, expected_value: Text, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"startswith": [jmespath, expected_value, message]}
        )
        return self

    def assert_endswith(
            self, jmespath: Text, expected_value: Text, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"endswith": [jmespath, expected_value, message]}
        )
        return self

    def assert_regex_match(
            self, jmespath: Text, expected_value: Text, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"regex_match": [jmespath, expected_value, message]}
        )
        return self

    def assert_contains(
            self, jmespath: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self.__step_context.validators.append(
            {"contains": [jmespath, expected_value, message]}
        )
        return self

    def perform(self) -> TStep:
        return self.__step_context


class StepRequestExtraction:
    def __init__(self, step_context: TStep):
        self.__step_context = step_context

    def with_jmespath(self, jmespath: Text, var_name: Text) -> "StepRequestExtraction":
        self.__step_context.extract[var_name] = jmespath
        return self

    def with_regex(self):
        # TODO: extract response html with regex
        pass

    def with_jsonpath(self):
        # TODO: extract response json with jsonpath
        pass

    def validate(self) -> StepRequestValidation:
        return StepRequestValidation(self.__step_context)

    def perform(self) -> TStep:
        return self.__step_context


class RequestWithOptionalArgs:
    """
    将可选参数填充到请求对象
    """

    def __init__(self, step_context: TStep):
        self.__step_context = step_context

    def with_params(self, **params) -> 'RequestWithOptionalArgs':
        self.__step_context.request.params.update(params)
        return self

    def with_data(self, data) -> 'RequestWithOptionalArgs':
        self.__step_context.request.data = data
        return self

    def with_json(self, json) -> 'RequestWithOptionalArgs':
        self.__step_context.request.req_json = json
        return self

    def with_headers(self, **headers) -> 'RequestWithOptionalArgs':
        self.__step_context.request.headers.update(headers)
        return self

    def with_cookies(self, **cookies) -> 'RequestWithOptionalArgs':
        self.__step_context.request.cookies.update(cookies)
        return self

    def with_files(self, **files) -> 'RequestWithOptionalArgs':
        self.__step_context.request.files.update(files)
        return self

    def set_timeout(self, timeout: float) -> 'RequestWithOptionalArgs':
        self.__step_context.request.timeout = timeout
        return self

    def set_allow_redirects(self, allow_redirects: bool) -> 'RequestWithOptionalArgs':
        self.__step_context.request.allow_redirects = allow_redirects
        return self

    def set_verify(self, verify: bool) -> 'RequestWithOptionalArgs':
        self.__step_context.request.verify = verify
        return self

    def extract(self) -> StepRequestExtraction:
        return StepRequestExtraction(self.__step_context)

    def validate(self):
        return StepRequestValidation(self.__step_context)

    def perform(self) -> TStep:
        return self.__step_context


# 创建RunRequest对象时，在RunRequest类的初始化函数中创建一个TStep对象，通过调用get等方法创建一个TRequest对象
class RunRequest:
    """
    创建请求步骤及请求对象
    """

    def __init__(self, name: Text):
        # 创建一个TStep对象
        self.__step_context = TStep(name=name)

    def get(self, url: Text) -> RequestWithOptionalArgs:
        self.__step_context.request = TRequest(method=RequestMethod.GET, url=url)
        return RequestWithOptionalArgs(self.__step_context)

    def post(self, url: Text) -> RequestWithOptionalArgs:
        self.__step_context.request = TRequest(method=RequestMethod.POST, url=url)
        return RequestWithOptionalArgs(self.__step_context)

    def put(self, url: Text) -> RequestWithOptionalArgs:
        self.__step_context.request = TRequest(method=RequestMethod.PUT, url=url)
        return RequestWithOptionalArgs(self.__step_context)

    def head(self, url: Text) -> RequestWithOptionalArgs:
        self.__step_context.request = TRequest(method=RequestMethod.HEAD, url=url)
        return RequestWithOptionalArgs(self.__step_context)

    def delete(self, url: Text) -> RequestWithOptionalArgs:
        self.__step_context.request = TRequest(method=RequestMethod.DELETE, url=url)
        return RequestWithOptionalArgs(self.__step_context)

    def options(self, url: Text) -> RequestWithOptionalArgs:
        self.__step_context.request = TRequest(method=RequestMethod.OPTIONS, url=url)
        return RequestWithOptionalArgs(self.__step_context)

    def patch(self, url: Text) -> RequestWithOptionalArgs:
        self.__step_context.request = TRequest(method=RequestMethod.PATCH, url=url)
        return RequestWithOptionalArgs(self.__step_context)


# 用户操作更加方便，增强代码的可读性，对TStep做一层封装

class Step:
    def __init__(
            self,
            step_context: Union[
                StepRequestExtraction,
                StepRequestValidation,
                RequestWithOptionalArgs,
            ],
    ):
        self.__step_context = step_context.perform()

    def perform(self) -> TStep:
        return self.__step_context

# 用例：有两个操作步骤
#
# s1 = Step(
#     RunRequest('获取验证码').get('http://www.huicewang.com')
# )
# s1.perform()
# s2 = Step(
#     RunRequest('注册').post('').with_data('').validate().assert_equal('')
# )
