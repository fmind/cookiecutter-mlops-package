# https://just.systems/man/en/

# REQUIRES

find := require("find")
rm := require("rm")
uv := require("uv")

# DEFAULTS

# display help information
default:
    @just --list

# TASKS

# clean the project
clean:
    rm -rf .venv/
    rm -rf .mypy_cache/
    rm -rf .pytest_cache/

# install the project
install:
    uv sync --all-groups

# setup the project hooks
hooks:
    uv run pre-commit install

# run the project unit tests
test:
    uv run pytest tests/
