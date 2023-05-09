# ----------------------------------------------------------------------
# OS dependent configuration
# ----------------------------------------------------------------------

VENV=venv/bin/
LIB=venv/Lib/site-packages/
MARKER=venv/marker
EXE=
ifeq ($(OS),Windows_NT)
VENV=venv/Scripts/
LIB=venv/Lib/site-packages/
MARKER=venv/marker
EXE=.exe
endif


# ----------------------------------------------------------------------
# Python interpreter detection
# ----------------------------------------------------------------------

ARG_COMMAND="import sys;print(sys.version_info>=(3, 8))"

ifeq (ok,$(shell test -e /dev/null 2>&1 && echo ok))
NULL_STDERR=2>/dev/null
else
NULL_STDERR=2>NUL
endif

ifndef PY

ifndef _PY
ifeq (True,$(shell py -3 -c $(ARG_COMMAND) $(NULL_STDERR)))
_PY=py -3
endif
endif

ifndef _PY
ifeq (True,$(shell python3 -c $(ARG_COMMAND) $(NULL_STDERR)))
_PY=python3
endif
endif

ifndef _PY
ifeq (True,$(shell python -c $(ARG_COMMAND) $(NULL_STDERR)))
PY=python
endif

endif

ifndef _PY
$(error Could not detect Python 3.8 or greather interpreter automatically, please use PY environment variable.)
endif

PY=$(_PY)

endif

ifneq (True,$(shell $(PY) -c $(ARG_COMMAND) $(NULL_STDERR)))
$(error $(PY) is not a valid Python 3.8 or greather interpreter)
endif

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

GIT=git
PIP=$(PY) -m pip
VENV_PY=$(VENV)python$(EXE)
VENV_PIP=$(VENV)pip$(EXE)

RM_GLOB := $(PY) -c "import shutil,sys,pathlib;[shutil.rmtree(sp, ignore_errors=False)for p in sys.argv[1:]for sp in pathlib.Path().resolve().glob(p)]"
BROWSER := $(PY) -c "import os,webbrowser,sys;from urllib.request import pathname2url;webbrowser.open('file:'+pathname2url(os.path.abspath(sys.argv[1])))"
EXTRACT_HELP := $(PY) -c "import re,sys;m=[re.match(r'^([a-zA-Z_-]+):.*?\#\# (.*)$$',line)for line in sys.stdin];print('\n'.join('{:12} {}'.format(*g.groups())for g in m if g))"
LS := $(PY) -c "import sys,os;print('\n'.join(os.listdir(os.path.abspath(sys.argv[1]))))"
TOUCH := $(PY) -c "import sys;open(sys.argv[1], 'ab')"

TOX=$(VENV)tox$(EXE)
SPHINX=$(VENV)sphinx-build$(EXE)
COVERAGE=$(VENV)coverage$(EXE)
TWINE=$(VENV)twine$(EXE)
PRECOMMIT=$(VENV)pre-commit$(EXE)


# ----------------------------------------------------------------------
# Automatic installation
# ----------------------------------------------------------------------

.git:
	$(GIT) init
	$(GIT) add *
	$(GIT) commit -m "Initial commit"
	$(GIT) branch -M main

$(MARKER): pyproject.toml .git
	$(PIP) install virtualenv
	$(PY) -m virtualenv venv
	$(VENV_PIP) install 'setuptools>=62.0.0' 'pip>=21.3'
	$(VENV_PIP) install -e .[pre-commit,lint]
	$(PRECOMMIT) install
	$(TOUCH) $(MARKER)

$(VENV): $(MARKER)

$(VENV_PY): $(MARKER)

$(VENV_PIP): $(MARKER)

$(TOX): $(VENV_PIP)
	$(VENV_PIP) install -e .[tox]

$(PRECOMMIT): $(VENV_PIP)

$(SPHINX): $(VENV_PIP)
	$(VENV_PIP) install -e .[docs]

$(COVERAGE): $(VENV_PIP)
	$(VENV_PIP) install -e .[cov]

$(TWINE): $(VENV_PIP)
	$(VENV_PIP) install -e .[deploy]

$(LIB)build: $(VENV_PIP)
	$(VENV_PIP) install -e .[build]


# ----------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------

.PHONY: help setup clean purge format lint tests-all tests coverage docs open-docs dist release install
.DEFAULT_GOAL := help

clean:  ## Remove all build, test, coverage, venv and Python artifacts.
	$(RM_GLOB) 'venv/*/python.?e?x?e?' 'venv' 'build/' 'dist/' 'public/' '.eggs/' '.tox/' '.coverage' 'htmlcov/' '.pytest_cache' '.mypy_cache' '.ruff_cache'  '**/*.egg-info' '**/*.egg' '**/__pycache__' '**/*~' '**/*.pyc' '**/*.pyo'

cov: $(COVERAGE)  ## Check code coverage.
	$(COVERAGE) run --source minelog -m pytest
	$(COVERAGE) report -m
	$(COVERAGE) html

dist: clean $(LIB)build  ## Builds source and wheel package.
	$(VENV_PY) -m build
	$(LS) dist/

docs: $(SPHINX) ## Generate Sphinx HTML documentation.
	$(SPHINX) -W -b html docs public

format: $(PRECOMMIT)  ## Format style with pre-commit, ruff, black and mypy.
	$(PRECOMMIT) run --all-files

help:  ## Show current message.
	@$(EXTRACT_HELP) < $(MAKEFILE_LIST)

install:  ## Install the package to the active Python's site-packages.
	$(PIP) install .

lint: $(TOX)  ## Check style with tox, ruff, black and mypy.
	$(TOX) -e lint

open-docs: docs  ## Open documentation.
	$(BROWSER) public/index.html

open-cov: cov  ## Open coverage report.
	$(BROWSER) htmlcov/index.html

release: dist $(TWINE)  ## Package and upload a release.
	$(TWINE) upload dist/*

setup: clean $(VENV_PY)  ## Create virtual environment and install pre-commit.

tests: $(TOX)  ## Run unit and functional tests.
	$(TOX) -e tests

tests-all: $(TOX)  ## Run all tests in parallel (docs, lint and tests).
	$(TOX) -p
