# ----------------------------------------------------------------------
# Python interpreter detection
# ----------------------------------------------------------------------

ifeq (ok,$(shell test -e /dev/null 2>&1 && echo ok))
NULL_STDERR=2>/dev/null
else
NULL_STDERR=2>NUL
endif

ifndef PY
ifeq (1,$(shell python3.8 -c "print(1)" $(NULL_STDERR)))
PY=python3.8
endif
endif

ifndef PY
ifeq (1,$(shell python3 -c "print(1)" $(NULL_STDERR)))
PY=python3
endif
endif

ifndef PY
ifeq (1,$(shell py -3.8 -c "print(1)" $(NULL_STDERR)))
PY=py -3.8
endif
endif

ifndef PY
ifeq (1,$(shell py -3 -c "print(1)" $(NULL_STDERR)))
PY=py -3
endif
endif

ifndef PY
ifeq (1,$(shell python -c "print(1)" $(NULL_STDERR)))
PY=python
endif
endif

ifndef PY
$(error Could not detect Python interpreter automatically, please use PY environment variable.)
endif


# ----------------------------------------------------------------------
# OS dependent configuration
# ----------------------------------------------------------------------

ifeq (win32,$(shell $(PY) -c "print(__import__('sys').platform)"))
VENV=venv\\Scripts\\
VENV_ACTIVATE=$(VENV)Activate.ps1
else
VENV=venv/bin/
VENV_ACTIVATE=$(VENV)activate
endif


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

GIT=git
PIP=$(PY) -m pip
VENV_PY=$(VENV)python
VENV_PIP=$(VENV_PY) -m pip
DEPS=pyproject.toml

.PHONY: help clean coverage dist docs install lint venv
.DEFAULT_GOAL := help

RM_GLOB := $(PY) -c "import shutil,sys,pathlib;[shutil.rmtree(sp, ignore_errors=True)for p in sys.argv[1:]for sp in pathlib.Path().resolve().glob(p)]"
BROWSER := $(PY) -c "import os,webbrowser,sys;from urllib.request import pathname2url;webbrowser.open('file:'+pathname2url(os.path.abspath(sys.argv[1])))"
EXTRACT_HELP := $(PY) -c "import re,sys;m=[re.match(r'^([a-zA-Z_-]+):.*?\#\# (.*)$$',line)for line in sys.stdin];print('\n'.join('{:12} {}'.format(*g.groups())for g in m if g))"
LS := $(PY) -c "import sys,os;print('\n'.join(os.listdir(os.path.abspath(sys.argv[1]))))"


# ----------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------

help:  ## Show current message
	@$(EXTRACT_HELP) < $(MAKEFILE_LIST)

.git:
	$(GIT) init
	$(GIT) add *
	$(GIT) commit -m "Initial commit"
	$(GIT) branch -M main

$(VENV_ACTIVATE): $(DEPS) .git
	$(MAKE) clean
	$(PY) -m venv venv
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -e .[dev]
	$(VENV)pre-commit install

setup: $(VENV_ACTIVATE)  ## Create virtual environment and install all the stuff

clean:  ## Remove all build, test, coverage and Python artifacts
	$(RM_GLOB) 'build/' 'dist/' 'public/' '.eggs/' '.tox/' '.coverage' 'htmlcov/' '.pytest_cache' '.mypy_cache' '.ruff_cache' '.venv' 'venv' '**/*.egg-info' '**/*.egg' '**/__pycache__' '**/*~' '**/*.pyc' '**/*.pyo'

format: setup  ## Fromat style with pre-commit, ruff, black and mypy
	$(VENV)pre-commit run --all-files

lint: setup  ## Check style with ruff, black and mypy
	$(VENV)tox -e lint

tests-all: setup  ## Run all tests
	$(VENV)tox -p

tests: setup  ## Run tests
	$(VENV)tox -e tests

coverage: setup  ## Check code coverage quickly with the default Python
	$(VENV)coverage run --source minelog -m pytest
	$(VENV)coverage report -m
	$(VENV)coverage html
	$(BROWSER) htmlcov/index.html

docs: setup  ## Generate Sphinx HTML documentation
	$(VENV)sphinx-build -W -b html docs public

open-docs: docs  ## Open docs
	$(BROWSER) public/index.html

dist: clean setup  ## Builds source and wheel package
	$(VENV_PY) -m build
	$(LS) dist/

release: dist  ## Package and upload a release
	$(VENV)twine upload dist/*

install: clean  ## Install the package to the active Python's site-packages
	$(PIP) install .
