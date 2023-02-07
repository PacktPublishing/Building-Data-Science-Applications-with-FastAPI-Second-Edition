set dotenv-load := false

default:
  @just --list

lint:
  black .
  ruff --fix .
  mypy chapter*/

lint-check:
  black --check .
  ruff .
  mypy chapter*/

test:
  pytest
