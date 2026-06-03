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
.. |docs| image:: https://readthedocs.org/projects/lazy_qa/badge/?style=flat
    :target: https://lazy_qa.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/angeleyesffx/lazy_qa/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/angeleyesffx/lazy_qa/actions

.. |requires| image:: https://requires.io/github/angeleyesffx/lazy_qa/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/angeleyesffx/lazy_qa/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/angeleyesffx/lazy_qa/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/angeleyesffx/lazy_qa

.. |version| image:: https://img.shields.io/pypi/v/lazy-qa.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/lazy-qa

.. |wheel| image:: https://img.shields.io/pypi/wheel/lazy-qa.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/lazy-qa

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/lazy-qa.svg
    :alt: Supported versions
    :target: https://pypi.org/project/lazy-qa

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/lazy-qa.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/lazy-qa

.. |commits-since| image:: https://img.shields.io/github/commits-since/angeleyesffx/lazy_qa/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/angeleyesffx/lazy_qa/compare/v0.0.0...master



.. end-badges

``lazy_qa`` is a Python utility package focused on QA and test automation workflows.
It centralizes common helpers used in API and data-driven testing, including payload
handling, data-file manipulation, request helpers, and random test data generation.

This repository is positioned as a practical QA automation toolkit: small reusable
functions that reduce repetitive setup effort in automated test projects.

Key capabilities
================

- **Data utilities** for CSV, JSON and YAML handling.
- **Request helpers** for request execution, payload compression and batched requests.
- **Database helpers** for MySQL and PostgreSQL access patterns used in tests.
- **List and string helpers** for common test data transformations.
- **CLI entrypoint** (`lazy-qa`) for command-line execution hooks.

License
=======

- Free software: MIT license

Installation
============

Install the published package:

.. code-block:: bash

    pip install lazy-qa

Install from source for local development:

.. code-block:: bash

    git clone https://github.com/angeleyesffx/lazy_qa.git
    cd lazy_qa
    pip install -e .


Quick usage examples
====================

Generate identifiers for test data:

.. code-block:: python

    from lazy_qa import generate_unique_id, generate_unique_email

    identifier = generate_unique_id(8)
    email = generate_unique_email("qa.user", identifier, ["@example.com"])

Work with JSON and CSV test resources:

.. code-block:: python

    from lazy_qa import load_json_as_dict, load_csv

    payload = load_json_as_dict("request_template.json")
    rows = load_csv("test_data.csv")

Compress payloads before API submission:

.. code-block:: python

    from lazy_qa import zip_payload

    compressed = zip_payload('{"event":"smoke-test"}')

Project structure
=================

.. code-block:: text

    src/lazy_qa/
      cli.py                   # package entrypoint
      csv_builder.py           # CSV helper functions
      json_builder.py          # JSON/template payload helpers
      request_builder.py       # HTTP request helper functions
      database_mysql.py        # MySQL helpers
      database_postgresql.py   # PostgreSQL helpers
      list_manipulation.py     # list utility functions
      string_manipulation.py   # string utility functions
      yaml_manipulation.py     # YAML helper functions
    tests/
      test_lazy_qa.py

Documentation
=============

https://lazy_qa.readthedocs.io/

Development
===========

Run tests:

.. code-block:: bash

    pytest -vv --ignore=src

Run project checks and full local matrix:

.. code-block:: bash

    tox

Future improvements
===================

- Expand automated unit coverage for utility modules.
- Improve CLI commands for common QA automation tasks.
- Harden request/database helpers with stricter validation and error handling.

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
