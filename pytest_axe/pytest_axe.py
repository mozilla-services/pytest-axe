# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from axe_selenium_python import Axe


@pytest.fixture
def axe(selenium, base_url):
    """Return an Axe instance based on context and options."""
    selenium.get(base_url)
    yield Axe(selenium)

def pytest_addoption(parser):
    parser.addoption("--axe", action="store_true", default=False,
                     help="run accessibility tests only")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--axe"):
        # --axe in cli: run accessibility tests and skip others
        skip_not_a11y = pytest.mark.skip(reason="run accessibility tests only.")
        for item in items:
            if "accessibility" not in item.keywords:
                item.add_marker(skip_not_a11y)
        return
    skip_a11y = pytest.mark.skip(reason="need --axe to run accessibility tests")
    for item in items:
        if "accessibility" in item.keywords:
            item.add_marker(skip_a11y)
