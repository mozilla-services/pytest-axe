# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from setuptools import setup


with open("./README.rst", "r") as f:
    readme = f.read()

setup(
    name="pytest-axe",
    use_scm_version=True,
    description="pytest plugin for axe-selenium-python",
    long_description=readme,
    url="http://github.com/kimberlythegeek/pytest-axe",
    author="Kimberly Sereduck",
    author_email="ksereduck@mozilla.com",
    packages=["pytest_axe"],
    install_requires=[
        "pytest-selenium>=1.12.0",
        "pytest>=3.0.0",
        "axe_selenium_python>=2.0.6",
    ],
    entry_points={"pytest11": ["axe = pytest_axe.pytest_axe"]},
    license="Mozilla Public License 2.0 (MPL 2.0)",
    keywords="axe-core selenium pytest-selenium accessibility automation mozilla",
)
