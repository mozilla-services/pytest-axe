pytest-axe
==========

pytest-axe provides a variety of features to simplify accessibility testing using ``axe-selenium-python``.

.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/mozilla-services/pytest-axe/blob/master/LICENSE.txt
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-axe.svg
   :target: https://pypi.org/project/pytest-axe/
   :alt: PyPI
.. image:: https://img.shields.io/pypi/wheel/pytest-axe.svg
   :target: https://pypi.org/project/pytest-axe/
   :alt: wheel
.. image:: https://img.shields.io/github/issues-raw/mozilla-services/pytest-axe.svg
   :target: https://github.com/mozilla-services/pytest-axe/issues
   :alt: Issues
.. image:: https://travis-ci.org/mozilla-services/pytest-axe.svg
   :target: https://travis-ci.org/mozilla-services/pytest-axe
   :alt: Travis
.. image:: https://api.dependabot.com/badges/status?host=github&repo=mozilla-services/axe-selenium-python
   :target: https://dependabot.com
   :alt: Dependabot
.. image:: https://pyup.io/repos/github/mozilla-services/pytest-axe/python-3-shield.svg
   :target: https://pyup.io/repos/github/mozilla-services/pytest-axe/
   :alt: Python 3

Requirements
------------

You will need the following prerequisites in order to use pytest-axe:

- Python 2.7 or 3.6
- axe-selenium-python >= 2.1.1
- The appropriate driver for the browser you intend to use, downloaded and added to your path, e.g. geckodriver for Firefox:
  - `geckodriver <https://github.com/mozilla/geckodriver/releases>`_ downloaded and `added to your PATH <https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path#answer-40208762>`_

Optional
--------

- pytest-selenium >= 3.0.0

**pytest-selenium is required to use the axe pytest fixture.**

- PyPOM >= 1.3.0

**PyPOM is required to use the run_axe helper method.**

Installation
------------

To install pytest-axe:

.. code-block:: bash

  $ pip install pytest-axe

Usage
------

``pytest-axe`` adds a command-line option for specifying whether or not to run accessibility tests.

Running pytest with ``--axe`` will run only tests marked as accessibility, i.e. ``@pytest.mark.accessibility``.

The absence of this command line option will run only tests **not** marked as accessibility.

``pytest-axe`` also includes a pytest fixture to handle set up and tear down.

The following example will run aXe-core against the entire page, and check for violations of any impact level.

.. code-block:: python

   import pytest

    @pytest.mark.nondestructive
    def test_header_accessibility(axe):
        violations = axe.run()
        assert len(violations) == 0, axe.report(violations)

You can also customize your accessibility tests by defining ``context``, ``options``, or ``impact``.

.. code-block:: python

   import pytest

    @pytest.mark.nondestructive
    def test_header_accessibility(axe):
        violations = axe.run('header', None, 'critical')
        assert len(violations) == 0, axe.report(violations)

**The above example runs aXe against only the content within the** ``<header>`` **tag, and filters for violations labeled** ``critical``.

For more information on ``context`` and ``options``, view the `aXe
documentation here <https://github.com/dequelabs/axe-core/blob/master/doc/API.md#parameters-axerun>`_.

The third parameter, ``impact``, allows you to filter violations by their impact
level. The options are ``'critical'``, ``'serious'`` and ``'minor'``, with the
default value set to ``None``.

This will filter violations for the impact level specified, and **all violations with a higher impact level**.

The axe fixture uses ``base_url`` defined in the pytest command or in a config file.

.. code-block:: bash

  $ pytest --base-url http://www.mozilla.com --driver Firefox test_accessibility.py

Parameterized Tests and Expected Failures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As of version 1.1.0, ``pytest-axe`` provides helper methods to generate individual tests for
each accessibility rule.

Generating test cases for each accessibility rule enables the ability to
mark specific **rules** as expected failures. To enable test parameterization,
parameterized tests should be defined in separate classes, with xfailed rules
set in the class-level `params` dictionary.


Example
*******

.. code-block::python
  import pytest
  from selenium import webdriver
  from pytest_axe.pytest_axe import PytestAxe as Axe
  from pytest_axe.parametrize_tests import *

  class TestHomePageAccessibility(object):
      params = {
          # Used by pytest-axe to generate tests and configure xfails
          "color-contrast": "Reason: GitHub issue #5014 https://github.com/mozilla-services/screenshots/issues/5014",
          "html-has-lang": "Reason: GitHub issue #5015 https://github.com/mozilla-services/screenshots/issues/5015",
          "landmark-one-main": "Reason: GitHub issue #5016 https://github.com/mozilla-services/screenshots/issues/5016",
          "link-name": "Reason: GitHub issue #5017 https://github.com/mozilla-services/screenshots/issues/5017",
          "meta-viewport": "Reason: GitHub issue #5018 https://github.com/mozilla-services/screenshots/issues/5018",
          "region": "Reason: GitHub issue #5016 https://github.com/mozilla-services/screenshots/issues/5016",
      }

      @pytest.mark.accessibility
      def test_home_page_accessibility(self, rule):
          """Run accessibility audits on the home page of Screenshots."""
          driver = webdriver.Firefox()
          driver.get("https://firefox.com")
          axe = Axe(driver)
          axe.inject()

          results = axe.run_single_rule(rule)
          assert len(results) == 0, home_page.report(results)

PyPOM Example
^^^^^^^^^^^^^^^^^^^^^

**These examples are dependent on the use of** `PyPOM <https://github.com/mozilla/PyPOM>`_ **, and assumes any** ``Page`` **object has a** ``selenium`` **object attribute.**

.. code-block::python
  from pytest_axe.pytest_axe import run_axe


  @pytest.mark.accessibility
  def test_login_page_accessibility(login_page):
    """Test login page for accessibility violations."""
    run_axe(login_page)

And with custom run options:

.. code-block::python
  from pytest_axe.pytest_axe import run_axe


  @pytest.mark.accessibility
  def test_login_page_accessibility(login_page):
      """Test login page header for critical accessibility violations."""
      run_axe(login_page, "header", None, "critical")

Recording Results
^^^^^^^^^^^^^^^^^^^

``pytest-axe`` checks for an environment variable ``ACCESSIBILITY_REPORTING``.

To enable writing the aXe JSON results to file, set ``ACCESSIBILITY_REPORTING=true``.

Currently, this will write the JSON files to the root of your test directory, with the page title and a timestamp as the file name.


Resources
---------

- `Issue Tracker <http://github.com/mozilla-services/pytest-axe/issues>`_
- `Code <http://github.com/mozilla-services/pytest-axe/>`_
- `axe-selenium-python <https://github.com/mozilla-services/axe-selenium-python>`_

CHANGELOG
----------

Version 1.1.3
^^^^^^^^^^^^^
- Modified the way that tests are generated. Rather than configuring xfails in conftest.py, they are defined as class-level variables.

Version 1.1.0
^^^^^^^^^^^^^
- Added the ability to generate indiviudal test cases for each accessibility rule, which enables xfailing specific accessibility rules.

Version 1.0.0
^^^^^^^^^^^^^^
- Transferred functions and methods from ``axe_selenium_python``.
- ``run_axe`` helper method, to simplify accessibility testing for test suites using PyPOM.
- ``run()`` method, which injects the aXe JavaScript, runs aXe against the page, filters the results based on a specified ``impact`` level, and returns a dictionary of only violations, with the ``ruleId`` as the key.
- ``impact_included``, used by ``run()`` to filter checks by a specificed impact level.
- Environment variable ``ACCESSIBILITY_REPORTING`` to enable recording results.
- ``analyze()``, which calls ``run()`` and writes the JSON results to file, if enabled using the environment variable.

Version 0.2.0
^^^^^^^^^^^^^^
- Added a command line argument to filter tests based on the presence or absence of a pytest accessibility marker.
