import re


def find_all_data(data, LB='', RB=''):
    rule = LB + r'(.+?)' + RB
    data_list = re.findall(rule, data)
    return data_list
