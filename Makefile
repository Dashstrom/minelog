# ----------------------------------------------------------------------
# Python interpreter detection
# ----------------------------------------------------------------------

ifeq (ok,$(shell test -e /dev/null 2>&1 && echo ok))
NULL_STDERR=2>/dev/null
else
NULL_STDERR=2>NUL
endif

ifndef PY
ifeq (1,$(shell python3 -c "print(1)" $(NULL_STDERR)))
PY=python3
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

PIP=$(PY) -m pip
VENV_PY=$(VENV)python
VENV_PIP=$(VENV_PY) -m pip
DEPS=$(wildcart *requirements*.txt)

.PHONY: help clean coverage dist docs install lint venv
.DEFAULT_GOAL := help

RM_GLOB := $(PY) -c "import shutil,sys,pathlib;[shutil.rmtree(sp, ignore_errors=True)for p in sys.argv[1:]for sp in pathlib.Path().resolve().glob(p)]"
BROWSER := $(PY) -c "import os,webbrowser,sys;from urllib.request import pathname2url;webbrowser.open('file:'+pathname2url(os.path.abspath(sys.argv[1])))"
EXTRACT_HELP := $(PY) -c "import re,sys;m=[re.match(r'^([a-zA-Z_-]+):.*?\#\# (.*)$$',line)for line in sys.stdin];print('\n'.join('{:12} {}'.format(*g.groups())for g in m if g))"
LS := $(PY) -c "import sys,os;print('\n'.join(os.listdir(os.path.abspath(sys.argv[1]))))"


# ----------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------

help:  ## show current message
	@$(EXTRACT_HELP) < $(MAKEFILE_LIST)

$(VENV_ACTIVATE): $(DEPS)
	$(MAKE) clean
	$(PY) -m venv venv
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements-dev.txt
	$(VENV_PIP) install -e .
	$(VENV)pre-commit install

setup: $(VENV_ACTIVATE)  ## create virtual environment and install pre-commit

clean:  ## remove all build, test, coverage and Python artifacts
	$(RM_GLOB) 'build/' 'dist/' '.eggs/' '.tox/' '.coverage' 'htmlcov/' '.pytest_cache' '.mypy_cache' '.ruff_cache' '.venv' 'venv' '**/*.egg-info' '**/*.egg' '**/__pycache__' '**/*~' '**/*.pyc' '**/*.pyo'

lint: setup  ## check style with pre-commit, ruff, black and mypy
	$(VENV)pre-commit run --all-files

tests: setup  ## run all tests
	$(VENV)tox -p

coverage: setup  ## check code coverage quickly with the default Python
	$(VENV)coverage run --source minelog -m pytest
	$(VENV)coverage report -m
	$(VENV)coverage html
	$(BROWSER) htmlcov/index.html

docs: setup  ## generate Sphinx HTML documentation
	$(VENV)sphinx-build -W -b html docs public
	$(BROWSER) public/index.html

dist: clean setup  ## builds source and wheel package
	$(VENV_PY) -m build
	$(LS) dist/

release: dist  ## package and upload a release
	$(VENV)twine upload dist/*

install: clean  ## install the package to the active Python's site-packages
	$(PIP) install .
