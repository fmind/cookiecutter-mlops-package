"""Test the project generation."""

# %% IMPORTS

from pytest_cookies.plugin import Cookies
from pytestshellutils.shell import Subprocess

# %% COMMANDS

COMMANDS = [
    "git init",
    "uv run invoke cleans.reset",
    "uv run invoke installs",
    "uv run invoke formats",
    "uv run invoke checks",
    "uv run invoke docs",
    "uv run invoke projects",
    "uv run invoke packages",
    "uv run invoke containers",
    "uv run invoke mlflow.doctor",
]

# %% TESTS


def test_project_generation(cookies: Cookies) -> None:
    """Test the generation of the project."""
    # given
    context  = {
        "user": "tester",
        "name": "MLOps 123",
        "license": "apache-2",
        "version": "1.0.0",
        "description": "A test project.",
        "python_version": "3.12",
        "mlflow_version": "2.19.0",
    }
    repository = context['name'].lower().replace(' ', '-')
    package = repository.replace('-', '_')
    # when
    result = cookies.bake(extra_context=context)
    # then
    # - cookies
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()
    assert result.project_path.name == repository
    assert result.context == {
        "user": context['user'],
        "name": context['name'],
        "repository": repository,
        "package": package,
        "license": context['license'],
        "version": context['version'],
        "description": context['description'],
        "python_version": context['python_version'],
        "mlflow_version": context['mlflow_version'],
    }
    # - commands
    shell = Subprocess(cwd=result.project_path)
    for command in COMMANDS:
        result = shell.run(*command.split())
        assert result.returncode == 0, f"Command failed: {command}"
