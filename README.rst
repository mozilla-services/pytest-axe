pytest-axe
==========

Pytest plugin for ``axe-selenium-python``. ``pytest-axe`` adds a pytest fixture
for Axe objects, to simplify running accessibility checks. Using this fixture
requires the use of pytest-selenium.

``pytest-axe`` also includes a command line option, ``--axe``, to keep
accessibility tests separate from functional tests.



.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/kimberlythegeek/pytest-axe/blob/master/LICENSE.txt
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-axe.svg
   :target: https://pypi.org/project/pytest-axe/
   :alt: PyPI
.. image:: https://img.shields.io/github/issues-raw/kimberlythegeek/pytest-axe.svg
   :target: https://github.com/kimberlythegeek/pytest-axe/issues
   :alt: Issues

Requirements
------------

You will need the following prerequisites in order to use pytest-axe:

- Python 2.7 or 3.6
- pytest-selenium >= 3.0.0
- axe-selenium-python

Installation
------------

To install pytest-axe:

.. code-block:: bash

  $ pip install pytest-axe

Usage
-----

To run tests using pytest-selenium (a dependency of axe-selenium-python), tests must be marked with the non-destructive pytest decorator:

.. code-block:: python

 @pytest.mark.nondestructive
 def test_my_test_function():
   assert true

Test suites using axe-selenium-python must import pytest and the Axe class.

pytest-selenium relies on the `base_url <https://github.com/pytest-dev/pytest-base-url>`_ fixture, which can be set in a configuration file, or as a command line argument.

.. code-block:: ini

 [pytest]
  base_url = http://www.example.com

.. code-block:: bash

  $ pytest --base-url http://www.example.com

aXe Command Line Option
************************
The ``@pytest.mark.accessibility`` marker must be added to all accessibility tests.

To run only  **non**-accessibility tests, run ``pytest`` as usual. To run only
accessibility tests, add ``--axe`` to your ``pytest`` command(s).

Example Test Function
*********************

*test_accessibility.py*

.. code-block:: python

  import pytest
  from axe_selenium_python import Axe
  import pytest_axe

  @pytest.mark.nondestructive
  def test_accessibility(self, axe):

    response = axe.execute()

    assert len(response['violations']) == 0, axe.report()


Resources
---------

- `Issue Tracker <http://github.com/kimberlythegeek/pytest-axe/issues>`_
- `Code <http://github.com/kimberlythegeek/pytest-axe/>`_
