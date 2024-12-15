"""Tasks of the project."""

# %% IMPORTS

from invoke import task
from invoke.context import Context

# %% TASKS


@task
def clean(ctx: Context) -> None:
    """Clean the project."""
    ctx.run("rm -rf .venv/")
    ctx.run("rm -rf .mypy_cache/")
    ctx.run("rm -rf .pytest_cache/")
    ctx.run("find . -type f -name '*.py[co]' -delete")
    ctx.run(r"find . -type d -name __pycache__ -exec rm -r {} \+")


@task
def install(ctx: Context) -> None:
    """Install the project."""
    ctx.run("uv sync --all-groups")


@task
def hooks(ctx: Context) -> None:
    """Setup the project hooks."""
    ctx.run("uv run pre-commit install")


@task
def test(ctx: Context) -> None:
    """Run the project unit tests."""
    ctx.run("uv run pytest tests/")
