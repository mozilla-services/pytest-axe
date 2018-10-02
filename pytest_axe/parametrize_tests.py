import os
import pytest
from selenium import webdriver
from axe_selenium_python import Axe


def format_parameter(rule, xfail_rules):
    return pytest.param(rule, marks=pytest.mark.xfail(reason=xfail_rules[rule]))


def axe_core_get_rules():
    os.environ["MOZ_HEADLESS"] = "1"
    driver = webdriver.Firefox()
    axe = Axe(driver)
    axe.inject()
    rules = driver.execute_script("return axe.getRules()")
    driver.close()
    return rules


def parametrized_accessibility_rules(metafunc):
    rules = axe_core_get_rules()
    from pprint import pprint

    list = []
    for rule in rules:
        list.append(rule["ruleId"])
    xfail_rules = metafunc.config.xfail_rules
    for key, value in xfail_rules.items():
        if key in list:
            list[list.index(key)] = format_parameter(key, xfail_rules)
    return list


def axe_run_only(rule):
    command = '{runOnly:{type: "rule", values: ["' + rule + '"]}}'
    return "return axe.run(" + command + ")"


def pytest_generate_tests(metafunc):
    rules = parametrized_accessibility_rules(metafunc)
    if "rule" in metafunc.funcargnames:
        metafunc.parametrize("rule", rules)
