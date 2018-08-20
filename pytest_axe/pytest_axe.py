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
    axe = PytestAxe(page.selenium, None, context, options, impact)
    axe.analyze()


class PytestAxe(Axe):

    def __init__(self, selenium, script_url=None, context=None, options=None, impact=None):
        super(PytestAxe, self).__init__(selenium)
        self.context = context
        self.options = options
        self.impact = impact

    def report(self, violations):
        """
        Return readable report of accessibility violations found.

        :param violations: Dictionary of violations.
        :type violations: dict
        :return report: Readable report of violations.
        :rtype: string
        """
        string = ''
        string += 'Found ' + str(len(violations)) + ' accessibility violations:'
        for violation, rule in violations.items():
            string += '\n\n\nRule Violated:\n' + rule['id'] + ' - ' + rule['description'] + \
                '\n\tURL: ' + rule['helpUrl'] + \
                '\n\tImpact Level: ' + rule['impact'] + \
                '\n\tTags:'
            for tag in rule['tags']:
                string += ' ' + tag
            string += '\n\tElements Affected:'
            i = 1
            for node in rule['nodes']:
                for target in node['target']:
                    string += '\n\t' + str(i) + ') Target: ' + target
                    i += 1
                for item in node['all']:
                    string += '\n\t\t' + item['message']
                for item in node['any']:
                    string += '\n\t\t' + item['message']
                for item in node['none']:
                    string += '\n\t\t' + item['message']
            string += '\n\n\n'
        return string

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
        elif impact == 'moderate' & rule['impact'] != 'minor':
            return True
        elif impact == 'serious':
            if rule['impact'] == 'serious' or rule['impact'] == 'critical':
                return True
        elif impact == 'critical' and rule['impact'] == 'critical':
            return True
        else:
            return False

    def analyze(self):
        """Run aXe accessibility checks, and write results to file."""
        violations = self.run()

        # Format file name based on page title and current datetime.
        t = time.strftime("%m_%d_%Y_%H:%M:%S")
        title = self.selenium.title
        title = re.sub('[\s\W]', '-', title)
        title = re.sub('(-|_)+', '-', title)

        # Output results only if reporting is enabled.
        if environ.get('ACCESSIBILITY_REPORTING') == 'true':
            # Write JSON results to file if recording enabled
            self.write_results('%s_%s.json' % (title, t), violations)
        assert len(violations) == 0, self.report(violations)
