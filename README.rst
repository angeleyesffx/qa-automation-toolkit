========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/qaforge/badge/?style=flat
    :target: https://qaforge.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/angeleyesffx/qaforge/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/angeleyesffx/qaforge/actions

.. |requires| image:: https://requires.io/github/angeleyesffx/qaforge/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/angeleyesffx/qaforge/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/angeleyesffx/qaforge/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/angeleyesffx/qaforge

.. |version| image:: https://img.shields.io/pypi/v/qaforge.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/qaforge

.. |wheel| image:: https://img.shields.io/pypi/wheel/qaforge.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/qaforge

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/qaforge.svg
    :alt: Supported versions
    :target: https://pypi.org/project/qaforge

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/qaforge.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/qaforge

.. |commits-since| image:: https://img.shields.io/github/commits-since/angeleyesffx/qaforge/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/angeleyesffx/qaforge/compare/v0.0.0...master



.. end-badges



* Free software: MIT license

Installation
============

::

    pip install qaforge

You can also install the in-development version with::

    pip install https://github.com/angeleyesffx/qaforge/archive/master.zip


Documentation
=============


https://qaforge.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
