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

class PytestAxe(Axe):

    def __init__(self, selenium):
        super(PytestAxe, self).__init__(selenium)

    def get_rules(self):
        """Return array of accessibility rules."""
        response = self.selenium.execute_script('return axe.getRules();')
        return response

    def run(self, context=None, options=None, impact=None):
        """
        Inject aXe, run against current page, and return rules & violations.
        """
        self.inject()
        data = self.execute(context, options)
        violations = dict((rule['id'], rule) for rule in data['violations'] if self.impact_included(rule, impact))

        return violations

    def impact_included(self, rule, impact):
        """
        Function to filter for violations with specified impact level, and all
        violations with a higher impact level.
        """
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

    def analyze(self, context=None, options=None, impact=None):
        """Run aXe accessibility checks, and write results to file."""
        disabled = environ.get('ACCESSIBILITY_DISABLED')
        if not disabled or disabled is None:
            violations = self.run(context, options, impact)

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
