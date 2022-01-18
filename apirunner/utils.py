import copy
import allure
from apirunner.models import VariablesMapping, TConfig, TStep


def report_allure(config: TConfig = None, step: TStep = None):
    if config:
        allure.dynamic.feature(config.feature)
        allure.dynamic.story(config.story)
        allure.dynamic.title(config.name)
        allure.dynamic.severity(config.severity)
    if step:
        allure.step(step.name)


def merge_variables(
        variables: VariablesMapping, variables_to_be_overridden: VariablesMapping
) -> VariablesMapping:
    """ merge two variables mapping, the first variables have higher priority
    """
    step_new_variables = {}
    for key, value in variables.items():
        if f"${key}" == value or "${" + key + "}" == value:
            # e.g. {"base_url": "$base_url"}
            # or {"base_url": "${base_url}"}
            continue

        step_new_variables[key] = value

    merged_variables = copy.copy(variables_to_be_overridden)
    merged_variables.update(step_new_variables)
    return merged_variables
