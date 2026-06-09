========
qaforge
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - |github-actions| |codecov|
    * - package
      - |version| |supported-versions|

.. |github-actions| image:: https://github.com/angeleyesffx/qaforge/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/angeleyesffx/qaforge/actions

.. |codecov| image:: https://codecov.io/gh/angeleyesffx/qaforge/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/angeleyesffx/qaforge

.. |version| image:: https://img.shields.io/pypi/v/qaforge.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/qaforge

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/qaforge.svg
    :alt: Supported versions
    :target: https://pypi.org/project/qaforge

.. end-badges

A Python toolkit providing reusable helpers for QA automation projects.
Originally extracted from a Behave-based test framework's Base Page Object,
qaforge centralises the utilities that every test project ends up rewriting:
HTTP requests, payload templating, data manipulation, database access, and test data generation.

* Free software: MIT license
* Python: 3.9+

Installation
============

::

    pip install qaforge

To install the development version directly from GitHub::

    pip install https://github.com/angeleyesffx/qaforge/archive/master.zip


Modules
=======

request_builder
---------------

Send HTTP requests and handle authentication flows.

.. code-block:: python

    from qaforge.request_builder import get_access_token, select_request

    # Retrieve a bearer token
    token = get_access_token(
        key="access_token",
        method="post",
        url="https://auth.example.com/token",
        payload={"client_id": "...", "client_secret": "..."},
    )

    headers = {"Authorization": f"Bearer {token}"}

    # Send a single request
    response = select_request("post", "https://api.example.com/users", payload, headers)

    # Send the same request against multiple payloads
    responses = select_request("post", url, payloads, headers, multiple_request=True)

    # Disable SSL verification for environments with self-signed certificates
    response = select_request("get", url, None, headers, verify=False)

json_builder
------------

Build, edit, and render JSON payloads — including Jinja2 template support.

.. code-block:: python

    from qaforge.json_builder import (
        load_json_as_dict,
        edit_template_json,
        create_payload,
    )

    # Load a JSON file as a Python dict
    data = load_json_as_dict("fixtures/user.json")

    # Edit specific keys in a JSON template file
    updated = edit_template_json("fixtures/user.json", {"name": "Alice", "role": "admin"})

    # Render a Jinja2 JSON template and get a beautified payload
    # Expects a templates/ directory relative to the working directory
    payload = create_payload("create_user", {"name": "Alice"}, multiple_request=False)

csv_builder
-----------

Read CSV files into JSON-serialisable structures.

.. code-block:: python

    from qaforge.csv_builder import load_csv, get_scenario_data_csv

    # All rows as a list of JSON strings
    rows = load_csv("data/users.csv")

    # Filter rows by test scenario ID
    rows = get_scenario_data_csv("data/scenarios.csv", "scenario_login_valid")

    # Read and group multi-row records
    from qaforge.csv_builder import load_csv_multiple_lines
    orders = load_csv_multiple_lines("data/orders.csv", ["order_id"], "items", ["product", "qty"])

yaml_manipulation
-----------------

Read YAML configuration files used as test environment descriptors.

.. code-block:: python

    from qaforge.yaml_manipulation import read_yml_file, select_the_keys_from_yml

    config = read_yml_file("config/environments.yml")

    # Get all top-level keys (e.g. list of environments)
    envs = select_the_keys_from_yml("config/environments.yml", "environment")

    # Get all keys nested under every top-level group
    all_keys = select_the_keys_from_yml("config/environments.yml", "other")

string_manipulation
-------------------

Generate unique test identifiers, emails, and manipulate strings.

.. code-block:: python

    from qaforge.string_manipulation import (
        generate_unique_id,
        generate_unique_email,
        generate_random_number,
        split_string_between,
        empty_string_to_none_string,
    )

    uid = generate_unique_id(12)                          # "aB3xKp9mQrLz"
    email = generate_unique_email("user", uid, ["@qa.io", "@test.com"])
    number = generate_random_number(6)                    # "482917"
    token = split_string_between(response_body, '"token":"', '"')
    value = empty_string_to_none_string(api_field)        # None if blank

list_manipulation
-----------------

Work with datapools — dictionaries of named test data sets.

.. code-block:: python

    from qaforge.list_manipulation import datapool_read, get_list_from_source

    datapool = {
        "valid_user": [{"username": "alice", "password": "secret"}],
        "admin_user": [{"username": "admin", "password": "admin123"}],
    }

    username = datapool_read(datapool, "valid user", "username")  # "alice"
    record   = get_list_from_source(datapool, "admin user")       # {"username": "admin", ...}

database_mysql
--------------

Run queries against a MySQL database.

.. code-block:: python

    from qaforge.database_mysql import execute_query_from_db, select_all_from_table

    rows = execute_query_from_db(
        host="localhost", port=3306,
        username="qa", password="qa",
        database="app_test",
        sql_query="SELECT * FROM orders WHERE status = 'pending'",
    )

    conn = open_mysql_connection("localhost", 3306, "qa", "qa", "app_test")
    all_rows = select_all_from_table(conn, "users")

database_postgresql
-------------------

Run queries against a PostgreSQL database.

.. code-block:: python

    from qaforge.database_postgresql import execute_query

    rows = execute_query(
        host="localhost",
        dbname="app_test",
        user="qa",
        password="qa",
        sql_query="SELECT id, email FROM users WHERE active = true",
    )


Development
===========

Setup::

    git clone https://github.com/angeleyesffx/qaforge.git
    cd qaforge
    pip install -e . -r requirements-dev.txt

Run the test suite::

    pytest tests/ -v

Run with coverage::

    pytest tests/ --cov=src/qaforge --cov-report=term-missing

The project targets Python 3.9–3.12 and is tested on all four versions via GitHub Actions on every push and pull request.
