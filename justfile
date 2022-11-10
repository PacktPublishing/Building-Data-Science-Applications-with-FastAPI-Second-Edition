set dotenv-load := false

default:
  @just --list

lint:
  isort .
  black .
  ruff --fix .
  mypy .

lint-check:
  isort --check .
  black --check .
  ruff .
  mypy .

test:
  pytest
