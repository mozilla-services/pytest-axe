# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from os import path
import pytest
import json

filename = "results.json"
if filename:
    with open(filename, "r") as f:
        test_data = json.load(f)


def test_report(axe):
    """Test that report exists."""
    violations = axe.run()

    report = axe.report(violations)
    assert report is not None, report


def test_run(base_url, axe):
    """Assert that run method returns results."""
    violations = axe.run()
    assert violations == test_data


@pytest.mark.skip
def test_impact_included():
    """Check that impact_included is correctly filtering violations."""
    assert True


@pytest.mark.skip
def test_analyze():
    assert True


def test_write_results(base_url, axe):
    """Assert that write results method creates a file."""
    axe.inject()
    data = axe.run()
    filename = "test.json"
    axe.write_results(filename, data)
    # check that file exists and is not empty
    assert path.exists(filename), "Output file not found."
    assert path.getsize(filename) > 0, "File contains no data."

    if filename:
        with open(filename, "r") as f:
            results = json.load(f)
    assert results == test_data
