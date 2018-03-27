# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import time
from os import environ

import pytest

from axe_selenium_python import Axe


@pytest.fixture
def axe(selenium, base_url):
    """Return an Axe instance based on context and options."""
    selenium.get(base_url)
    yield PytestAxe(selenium)


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


def run_axe(page, context=None, options=None, impact=None):
    print("\nrun_axe: impact=%s" % impact)
    axe = PytestAxe(page.selenium)
    axe.analyze()


class PytestAxe(Axe):

    def __init__(self, selenium, script_url=None, context=None, options=None, impact=None):
        super(PytestAxe, self).__init__(selenium)
        self.context = context
        self.options = options
        self.impact = impact

    def get_rules(self):
        """Return array of accessibility rules."""
        response = self.selenium.execute_script('return axe.getRules();')
        return response

    def run(self):
        """Inject aXe, run against current page, and return rules & violations."""
        self.inject()
        data = self.execute(self.context, self.options)
        violations = dict((rule['id'], rule) for rule in data['violations'] if self.impact_included(rule))

        return violations

    def impact_included(self, rule):
        """Filter violations with specified impact level or higher."""
        impact = self.impact
        if impact == 'minor' or impact is None:
            return True
        elif impact == 'serious':
            if rule['impact'] != 'minor':
                return True
        elif impact == 'critical':
            if rule['impact'] == 'critical':
                return True
        else:
            return False

    def analyze(self):
        """Run aXe accessibility checks, and write results to file."""
        disabled = environ.get('ACCESSIBILITY_DISABLED')
        if not disabled or disabled is None:
            violations = self.run()

            # Format file name based on page title and current datetime.
            t = time.strftime("%m_%d_%Y_%H:%M:%S")
            title = self.selenium.title
            title = re.sub('[\s\W]', '-', title)
            title = re.sub('(-|_)+', '-', title)

            # Output results only if reporting is enabled.
            if environ.get('ACCESSIBILITY_REPORTING') == 'true':
                # Write JSON results to file if recording enabled
                self.write_results('results/%s_%s.json' % (title, t), violations)
            assert len(violations) == 0, self.report(violations)
