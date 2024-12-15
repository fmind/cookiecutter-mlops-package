"""Format tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% TASKS


@task
def imports(ctx: Context) -> None:
    """Format python imports with ruff."""
    ctx.run("uv run ruff check --select I --fix")


@task
def sources(ctx: Context) -> None:
    """Format python sources with ruff."""
    ctx.run("uv run ruff format src/ tasks/ tests/")


@task(pre=[imports, sources], default=True)
def all(_: Context) -> None:
    """Run all format tasks."""
