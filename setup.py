# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from setuptools import setup

def readme():
    with open('README.rst') as f:
        readme = f.read()
    with open('CHANGELOG.rst') as f:
        log = f.read()
    return readme + '\n\n' + log

setup(name='pytest-axe',
    version='0.2.0',
    description='pytest plugin for axe-selenium-python',
    long_description=readme(),
    url='http://github.com/kimberlythegeek/pytest-axe',
    author='Kimberly Pennington',
    author_email='kpennington@mozilla.com',
    packages=['pytest_axe'],
    install_requires=[
        'pytest-selenium>=1.10.0',
        'pytest>=3.1.1',
        'axe_selenium_python'
    ],
    entry_points={'pytest11': ['axe = pytest_axe.pytest_axe']},
    license='Mozilla Public License 2.0 (MPL 2.0)',
    keywords='axe-core selenium pytest-selenium accessibility automation mozilla')
