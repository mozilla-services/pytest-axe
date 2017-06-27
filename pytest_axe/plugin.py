# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import axe_selenium_python
import requests

@pytest.fixture(scope='session')
def script_url(request):
    """Return a script URL"""
    config = request.config
    script_url = config.getoption('script_url')
    if script_url is not None:
return script_url

@pytest.yield_fixture
def axe(selenium, script_url, context=None, options=None):
    """Return an Axe instance based on context and options."""
    script_url = script_url()
    a = Axe(selenium, script_url)
    yield a
