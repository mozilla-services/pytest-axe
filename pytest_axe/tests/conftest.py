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
