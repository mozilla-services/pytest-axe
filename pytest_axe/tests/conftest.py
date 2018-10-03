# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import pytest
from selenium import webdriver

from ..pytest_axe import PytestAxe as Axe

base_url = os.path.join(os.path.dirname(__file__), "index.html")


@pytest.fixture(scope="session", autouse=True)
def test_page():
    driver = webdriver.Firefox()
    driver.get("file://" + base_url)

    axe = Axe(driver)
    axe.inject()

    yield axe
    driver.close()


def pytest_configure(config):
    """
        Included rule ID of tests that are expected to fail as a key, with the
        github issue number as a value (or any other desired info as
        reason for failure), and pass to pytestconfig to generate the tests.

        Example:
            config.xfail_rules = {
                "meta-viewport": "Reason: GitHub issue #245"
            }
    """
    config.xfail_rules = {
        "bypass": "Reason: testing",
        "color-contrast": "Reason: testing",
        "html-has-lang": "Reason: testing",
        "image-alt": "Reason: testing",
        "label": "Reason: testing",
        "landmark-one-main": "Reason: testing",
        "link-in-text-block": "Reason: testing",
        "page-has-heading-one": "Reason: testing",
        "region": "Reason: testing",
        "td-has-header": "Reason: testing",
    }
    pytest.config = config
