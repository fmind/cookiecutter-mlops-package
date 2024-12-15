"""Commit tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% TASKS


@task
def info(ctx: Context) -> None:
    """Print a guide for messages."""
    ctx.run("uv run cz info")


@task
def bump(ctx: Context) -> None:
    """Bump the version of the package."""
    ctx.run("uv run cz bump", pty=True)


@task
def commit(ctx: Context) -> None:
    """Commit all changes with a message."""
    ctx.run("uv run cz commit", pty=True)


@task(pre=[commit], default=True)
def all(_: Context) -> None:
    """Run all commit tasks."""
