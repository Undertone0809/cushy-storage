.PHONY: help lock install pre-commit-install polish-codestyle formatting format check-codestyle test lint lint-fix docker-build docker-remove

SHELL := /usr/bin/env bash
PYTHON := python
OS := $(shell python -c "import sys; print(sys.platform)")
IMAGE := cushy_storage
VERSION := latest

ifeq ($(OS),win32)
	PYTHONPATH := $(shell python -c "import os; print(os.getcwd())")
    TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=cushy_storage tests/
else
	PYTHONPATH := `pwd`
    TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=cushy_storage tests/
endif


help:
	@echo "Available commands:"
	@echo "  help              Show this help message"
	@echo "  lock              Update poetry.lock and requirements.txt"
	@echo "  install           Install dependencies using poetry"
	@echo "  pre-commit-install Install pre-commit hooks"
	@echo "  format            Format code using ruff"
	@echo "  test             Run tests with coverage"
	@echo "  lint             Run linting checks"
	@echo "  lint-fix         Fix linting issues"
	@echo "  docker-build     Build docker image"
	@echo "  docker-remove    Remove docker image"

lock:
	poetry lock -n && poetry export --without-hashes > requirements.txt

install:
	make lock
	poetry install -n

pre-commit-install:
	poetry run pre-commit install

polish-codestyle:
	poetry run ruff format --config pyproject.toml .
	poetry run ruff check --fix --config pyproject.toml .

formatting: polish-codestyle
format: polish-codestyle

test:
	$(TEST_COMMAND)
	poetry run coverage-badge -o assets/coverage.svg -f

check-codestyle:
	poetry run ruff format --check --config pyproject.toml .
	poetry run ruff check --config pyproject.toml .

lint: test check-codestyle

lint-fix: polish-codestyle

#* Docker
# Example: make docker-build VERSION=latest
# Example: make docker-build IMAGE=some_name VERSION=0.1.0
docker-build:
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

# Example: make docker-remove VERSION=latest
# Example: make docker-remove IMAGE=some_name VERSION=0.1.0
docker-remove:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)
