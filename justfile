set dotenv-load := false

default:
  @just --list

lint:
  black .
  ruff --fix .
  mypy .

lint-check:
  black --check .
  ruff .
  mypy .

test:
  pytest
