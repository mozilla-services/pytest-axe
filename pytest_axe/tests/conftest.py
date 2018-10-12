# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import pytest
from selenium import webdriver

from ..pytest_axe import PytestAxe as Axe

path_to_test_page_with_violations = os.path.join(
    os.path.dirname(__file__), "violations.html"
)
path_to_test_page_no_violations = os.path.join(
    os.path.dirname(__file__), "no_violations.html"
)


@pytest.fixture(scope="session", autouse=True)
def test_page_with_violations():
    driver = webdriver.Firefox()
    driver.get("file://" + path_to_test_page_with_violations)

    axe = Axe(driver)
    axe.inject()

    yield axe
    driver.close()


@pytest.fixture(scope="session", autouse=True)
def test_page_no_violations():
    driver = webdriver.Firefox()
    driver.get("file://" + path_to_test_page_no_violations)

    axe = Axe(driver)
    axe.inject()

    yield axe
    driver.close()
