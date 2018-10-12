# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import json
import os

from ..parameterize_tests import *  # NOQA

filename = os.path.join(os.path.dirname(__file__), "results.json")

if filename:
    with open(filename, "r") as f:
        test_data = json.load(f)


class TestPytestAxe(object):
    params = {
        "bypass": "Reason: testing",
        "html-has-lang": "Reason: testing",
        "image-alt": "Reason: testing",
        "label": "Reason: testing",
        "landmark-one-main": "Reason: testing",
        "page-has-heading-one": "Reason: testing",
        "region": "Reason: testing",
        "td-has-header": "Reason: testing",
    }

    def test_report(self, test_page_with_violations):
        """Test that report method returns a non-empty string."""
        violations = test_page_with_violations.run()
        report = test_page_with_violations.report(violations)
        assert report is not None

    def test_get_rules(self, test_page_with_violations):
        """Test that get_rules method returns a non-empty list."""
        rules = test_page_with_violations.get_rules()
        assert rules is not None

    def test_run(self, base_url, test_page_with_violations):
        """Assert that run method returns a non-empty dictionary."""
        violations = test_page_with_violations.run()
        assert violations is not None

    def test_xfail_parameterized_tests(self, rule, test_page_with_violations):
        """
            Test that parameterized tests xfail correctly, based on class-level
            params dictionary.
        """
        results = test_page_with_violations.run_single_rule(rule)
        assert len(results) == 0, test_page_with_violations.report(results)


class TestPytestAxeWithoutParams(object):
    def test_parameterized_tests_without_params(self, rule, test_page_no_violations):
        """Test that parameterization works correctly when params is not set."""
        results = test_page_no_violations.run_single_rule(rule)
        assert len(results) == 0, test_page_no_violations.report(results)
