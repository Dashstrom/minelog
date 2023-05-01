minelog
=======

.. image:: https://github.com/Dashstrom/blabla/actions/workflows/docs.yml/badge.svg
    :target: https://github.com/Dashstrom/blabla/actions/workflows/docs.yml
    :alt: CI : Docs

.. image:: https://github.com/Dashstrom/blabla/actions/workflows/lint.yml/badge.svg
    :target: https://github.com/Dashstrom/blabla/actions/workflows/lint.yml
    :alt: CI : Lint

.. image:: https://github.com/Dashstrom/blabla/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Dashstrom/blabla/actions/workflows/tests.yml
    :alt: CI : Tests

.. image:: https://github.com/Dashstrom/blabla/actions/workflows/publish.yml/badge.svg
    :target: https://github.com/Dashstrom/blabla/actions/workflows/publish.yml
    :alt: CI : Publish

.. image:: https://github.com/Dashstrom/blabla/actions/workflows/audit.yml/badge.svg
    :target: https://github.com/Dashstrom/blabla/actions/workflows/audit.yml
    :alt: CI : Audit

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

You can install "minelog" via `pip <https://pypi.org/project/pip/>`_ from `PyPI <https://pypi.org/project>`_

..  code-block:: bash

    pip install minelog

Usage
*******

Show all players IPs.

..  code-block:: bash

    minelog -d "..\logs" -p "^.* ([a-zA-Z0-9_]+)\[\/(.*\d+(?:\.\d+){3}):\d+\].*$" -u -s -r "\1,\2"
    minelog -d "..\logs" -p "^.*name=([a-zA-Z0-9_]+).*/(.*\d+(?:\.\d+){3}):\d+.*$" -u -s -r "\1,\2"


Developpement
*************

Contributing
------------
Contributions are very welcome. Tests can be run with tox, please ensure
the coverage at least stays the same before you submit a pull request.

Installation
------------

..  code-block:: bash

    sudo apt update -y && sudo apt upgrade -y
    sudo apt install mypy python3.8-venv
    git clone https://github.com/Dashstrom/minelog
    cd minelog
    make setup

Makefile
--------

A Makefile is available for help you to run commands.

..  code-block:: text

    help         show actual message
    venv         create virtual environment
    clean        remove all build, test, coverage and Python artifacts
    lint         check style with pre-commit
    test         run tests, lint and docs build
    coverage     check code coverage quickly with the default Python
    docs         generate Sphinx HTML documentation
    release      package and upload a release
    dist         builds source and wheel package
    install      install the package to the active Python's site-packages

License
*******

This work is licensed under `GNU GPL v3.0 <https://github.com/Dashstrom/minelog/blob/main/LICENSE>`_.
