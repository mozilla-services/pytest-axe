pytest-axe
==========

pytest-axe provides a variety of features to simplify accessibility testing using ``axe-selenium-python``.

.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg?style=for-the-badge
   :target: https://github.com/kimberlythegeek/pytest-axe/blob/master/LICENSE.txt
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-axe.svg?style=for-the-badge
   :target: https://pypi.org/project/pytest-axe/
   :alt: PyPI
.. image:: https://img.shields.io/github/issues-raw/kimberlythegeek/pytest-axe.svg?style=for-the-badge
   :target: https://github.com/kimberlythegeek/pytest-axe/issues
   :alt: Issues

Requirements
------------

You will need the following prerequisites in order to use pytest-axe:

- Python 2.7 or 3.6
- axe-selenium-python >= 2.0.1
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

``pytest-axe`` adds a command line option for specifying whether or not to run accessibility tests.

Running pytest with ``--axe`` will run only tests marked as accessibility, i.e. ``@pytest.mark.accessibility``.

The absence of this command line option will run only tests **not** marked as accessibility.

Pytest Fixture Example
^^^^^^^^^^^^^^^^^^^^^^^

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

PyPOM Example
^^^^^^^^^^^^^^^^^^^^^

**These examples are dependent on the use of** `PyPOM <https://github.com/mozilla/PyPOM>`_ **, and assumes any** ``Page`` **object has a** ``selenium`` **object attribute.**

.. code-block:: python

 from pytest_axe.pytest_axe import run_axe

  @pytest.mark.accessibility
  def test_login_page_accessibility(login_page):
      """Test login page for accessibility violations."""
      run_axe(login_page)

And with custom run options:

.. code-block:: python

 from pytest_axe.pytest_axe import run_axe

  @pytest.mark.accessibility
  def test_login_page_accessibility(login_page):
      """Test login page header for critical accessibility violations."""
      run_axe(login_page, 'header', None, 'critical')

Recording Results
^^^^^^^^^^^^^^^^^^^

``pytest-axe`` checks for an environment variable ``ACCESSIBILITY_REPORTING``.

To enable writing the aXe JSON results to file, set ``ACCESSIBILITY_REPORTING=true``.

Currently, this will write the JSON files to the root of your test directory, with the page title and a timestamp as the file name.


Resources
---------

- `Issue Tracker <http://github.com/kimberlythegeek/pytest-axe/issues>`_
- `Code <http://github.com/kimberlythegeek/pytest-axe/>`_
- `axe-selenium-python <https://github.com/mozilla-services/axe-selenium-python>`_
