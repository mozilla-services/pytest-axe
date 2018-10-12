# This module adds helper methods and pytest hooks to generate individual tests
# for each accessibility rule, and also enables xfailing specific rules.
import os

import pytest
from axe_selenium_python import Axe
from selenium import webdriver


def format_parameter(rule, xfail_rules):
    """
        Return a parameter that can be used by pytest_generate_tests to xfail
        test cases, as defined in the xfail_rules attribute of the pytest config
        object.
    """
    return pytest.param(rule, marks=pytest.mark.xfail(reason=xfail_rules[rule]))


def axe_core_get_rules():
    """Run aXe to get a current list of accessibility rules."""
    os.environ["MOZ_HEADLESS"] = "1"
    driver = webdriver.Firefox()
    axe = Axe(driver)
    axe.inject()
    rules = driver.execute_script("return axe.getRules()")
    driver.close()
    return rules


def parametrized_accessibility_rules(xfail_rules={}):
    """
        Get list of accessibility rules and modify it to xfail test cases as
        defined in the xfail_rules attribute of the pytest config object.
        (This is defined in the conftest.py file of your test suite.)

        Example:
        def pytest_configure(config):
            config.xfail_rules = {
                "meta-viewport": "Reason: GitHub issue #245"
            }
    """
    rules = axe_core_get_rules()
    list = []
    # Make a list containing only rule IDs.
    for rule in rules:
        list.append(rule["ruleId"])
    # Replace rule ID parameter with one containing xfail marker
    for rule, reason in xfail_rules.items():
        if rule in list:
            list[list.index(rule)] = format_parameter(rule, xfail_rules)
    return list


def pytest_generate_tests(metafunc):
    """Generate test cases from the formatted parameters."""
    rules = (
        parametrized_accessibility_rules(metafunc.cls.params)
        if hasattr(metafunc.cls, "params")
        else parametrized_accessibility_rules()
    )
    if "rule" in metafunc.funcargnames:
        metafunc.parametrize("rule", rules)
