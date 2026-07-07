"""Test the project generation."""

# %% IMPORTS

from pytest_cookies.plugin import Cookies
from pytestshellutils.shell import Subprocess

# %% COMMANDS

# `mise` is a system tool (not a uv dependency), so tasks run as `mise run <task>`.
# `git init` is required before `mise run install`: lefthook installs git hooks and
# `gitleaks` scans git history, both of which need a repository.
COMMANDS = [
    "mise trust -y",
    "git init",
    "mise run clean",
    "mise run install",
    "mise run format",
    "mise run check",
    "mise run docs",
    "mise run project",
    "mise run build",
    "mise run build:image",
    "mise run mlflow:doctor",
]

# %% TESTS


def test_project_generation(cookies: Cookies) -> None:
    """Test the generation of the project."""
    # given
    context = {
        "user": "tester",
        "name": "MLOps 123",
        "license": "MIT",
        "version": "1.0.0",
        "description": "A test project.",
        "python_version": "3.14",
        "mlflow_version": "3.14.0",
    }
    repository = context["name"].lower().replace(" ", "-")
    package = repository.replace("-", "_")
    # when
    result = cookies.bake(extra_context=context)
    # then
    # - cookies
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()
    assert result.project_path.name == repository
    assert result.context == {
        "user": context["user"],
        "name": context["name"],
        "package": package,
        "repository": repository,
        "license": context["license"],
        "version": context["version"],
        "description": context["description"],
        "python_version": context["python_version"],
        "mlflow_version": context["mlflow_version"],
        # cookiecutter keeps private keys in the rendered context.
        "_copy_without_render": ["cliff.toml"],
    }
    # - commands
    shell = Subprocess(cwd=result.project_path)
    for command in COMMANDS:
        result = shell.run(*command.split())
        assert result.returncode == 0, f"Command failed: {command}"
