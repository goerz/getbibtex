# Makefile for getbibtex development, built around uv.
#
# Run `make help` for an overview of the available targets.

.PHONY: help develop test test-lowest coverage \
        black black-check isort isort-check flake8 pylint lint \
        devrepl shell upgrade clean distclean

.DEFAULT_GOAL := help

# Python version for the development environment. Override on the command line,
# e.g. `make PYTHON=3.11 test`. uv downloads the interpreter if it is missing.
PYTHON ?= 3.12

# Dependency resolution strategy. Use `make RESOLUTION=lowest-direct test` to
# verify the project against the lowest declared dependency versions.
RESOLUTION ?= highest

# Each Python version gets its own environment so that switching PYTHON does not
# force a re-sync. `make distclean` removes the whole .venv tree.
export UV_PROJECT_ENVIRONMENT := .venv/py$(PYTHON)

# All development tooling lives in dependency groups (see pyproject.toml).
# `uv run` transparently creates and syncs the environment before running, and
# installs this project *editable*, so every target below picks up uncommitted
# source changes immediately, with no rebuild or reinstall step.
UV := uv run --python $(PYTHON) --resolution $(RESOLUTION) --all-groups

# Files checked by the test suite (modules and doctests in prose files).
TESTS ?= src tests README.md CONTRIBUTING.md

# Locations passed to the linters and formatters.
SOURCES ?= src tests

help:  ## Show this help
	@grep -E '^([a-zA-Z0-9_-]+):.*## ' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "%-20s %s\n", $$1, $$2}'

develop:  ## Create or sync the development environment
	uv sync --python $(PYTHON) --resolution $(RESOLUTION) --all-groups

test:  ## Run the test suite
	$(UV) pytest -v --durations=10 -x -s $(TESTS)

test-lowest:  ## Run the test suite against the lowest declared dependency versions
	$(MAKE) RESOLUTION=lowest-direct test

coverage:  ## Run tests with coverage; write HTML to ./htmlcov and coverage.xml
	$(UV) pytest -v --cov=getbibtex \
		--cov-report=term --cov-report=html --cov-report=xml $(TESTS)
	@echo "open htmlcov/index.html"

black:  ## Reformat the code with black
	$(UV) black $(SOURCES)

black-check:  ## Check code formatting with black
	$(UV) black --check --diff $(SOURCES)

isort:  ## Sort imports with isort
	$(UV) isort $(SOURCES)

isort-check:  ## Check import sorting with isort
	$(UV) isort --check-only --diff $(SOURCES)

flake8:  ## Check style with flake8
	$(UV) flake8 $(SOURCES)

pylint:  ## Check the code with pylint
	$(UV) pylint -j 0 src

lint: black-check isort-check flake8 pylint  ## Run all linters

devrepl:  ## Launch an IPython REPL with the editable package and dev tools
	$(UV) ipython

shell:  ## Open a shell inside the development environment
	$(UV) $$SHELL

upgrade:  ## Upgrade locked dependency versions to the latest compatible release
	uv lock --upgrade

clean:  ## Remove build, test, and coverage artifacts
	rm -rf build dist .eggs *.egg-info src/*.egg-info
	rm -rf .pytest_cache .coverage coverage.xml htmlcov .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

distclean: clean  ## Remove all generated files, including the .venv environments
	rm -rf .venv uv.lock .tox
