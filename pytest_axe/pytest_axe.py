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
