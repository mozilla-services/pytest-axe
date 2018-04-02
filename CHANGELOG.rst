CHANGELOG
----------

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
