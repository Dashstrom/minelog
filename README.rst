.. role:: bash(code)
   :language: bash

minelog
=======

.. image:: https://github.com/Dashstrom/minelog/actions/workflows/docs.yml/badge.svg
    :target: https://github.com/Dashstrom/minelog/actions/workflows/docs.yml
    :alt: CI : Docs
.. image:: https://github.com/Dashstrom/minelog/actions/workflows/lint.yml/badge.svg
    :target: https://github.com/Dashstrom/minelog/actions/workflows/lint.yml
    :alt: CI : Lint
.. image:: https://github.com/Dashstrom/minelog/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Dashstrom/minelog/actions/workflows/tests.yml
    :alt: CI : Tests
.. image:: https://img.shields.io/pypi/v/minelog.svg
    :target: https://pypi.org/project/minelog
    :alt: PyPI : minelog
.. image:: https://img.shields.io/pypi/pyversions/minelog.svg
    :target: https://pypi.org/project/minelog
    :alt: Python : versions
.. image:: https://img.shields.io/badge/license-GNU%20GPL%20v3.0-green.svg
    :target: https://github.com/Dashstrom/minelog/blob/main/LICENSE
    :alt: License : GNU GPL v3.0

Script for find somethings easily in your minecraft logs.

Install
*******

You can install :bash:`minelog` via `pip <https://pypi.org/project/pip/>`_ from `PyPI <https://pypi.org/project>`_

..  code-block:: bash

    pip install minelog

Usage
*****

Show all players IPs.

..  code-block:: bash

    minelog -d logs -p '^.* ([a-zA-Z0-9_]+)\[\/(.*\d+(?:\.\d+){3}):\d+\].*$' -u -s -r '\1,\2'
    minelog -d logs -p '^.*name=([a-zA-Z0-9_]+).*/(.*\d+(?:\.\d+){3}):\d+.*$' -u -s -r '\1,\2'

See below the help message.

..  code-block:: text

    Usage: minelog [OPTIONS]

      Script for find somethings easily in your minecraft logs.

    Options:
      --version             Show the version and exit.
      -d, --directory PATH  Path to logs.
      -p, --pattern TEXT    Pattern used for search log.
      -r, --repl TEXT       Replacement of match.
      -u, --unique          Return only unique match.
      -s, --sort            Sort match in alphabetical order.
      --help                Show this message and exit.

      Copyright 2023, Dashstrom <dashstrom.pro@gmail.com>


Developpement
*************

Contributing
------------

Contributions are very welcome. Tests can be run with :bash:`make tests-all`, please ensure
the coverage at least stays the same before you submit a pull request.

Developpement installation
--------------------------

..  code-block:: bash

    sudo apt update -y && sudo apt upgrade -y && sudo apt-get install python3-pip
    git clone https://github.com/Dashstrom/minelog && cd minelog
    make setup

Makefile
--------

A Makefile is available for help you to run commands.

..  code-block:: text

    clean        Remove all build, test, coverage, venv and Python artifacts.
    cov          Check code coverage.
    dist         Builds source and wheel package.
    docs         Generate Sphinx HTML documentation.
    format       Format style with pre-commit, ruff, black and mypy.
    help         Show current message.
    install      Install the package to the active Python's site-packages.
    lint         Check style with tox, ruff, black and mypy.
    open-docs    Open documentation.
    open-cov     Open coverage report.
    recreate     Clean project and recrete venv.
    release      Package and upload a release.
    setup        Create virtual environment and install pre-commit.
    tests        Run unit and functional tests.
    tests-all    Run all tests in parallel (docs, lint and tests).

License
*******

This work is licensed under `GNU GPL v3.0 <https://github.com/Dashstrom/minelog/blob/main/LICENSE>`_.
