"""Test the project generation."""

# %% IMPORTS

import json
import os
from pathlib import Path

from pytest_cookies.plugin import Cookies
from pytestshellutils.customtypes import EnvironDict
from pytestshellutils.shell import Subprocess

# %% COMMANDS

# `mise` is a system tool (not a uv dependency), so tasks run as `mise run <task>`.
# `mise install` is explicit: the generated project sets `run_auto_install = false`, so
# without it `mise run check` would not provision actionlint/zizmor/hadolint/trivy and
# would either error or silently fall through to whatever the outer shell happens to
# have on PATH — a green run that proves nothing about the generated project.
# `git init` is required before `mise run install`: lefthook installs git hooks and
# `gitleaks` scans git history, both of which need a repository.
COMMANDS = [
    "mise trust -y",
    "mise install -y",
    "git init",
    "mise run clean",
    "mise run install",
    # Stage the fresh project so the diff below catches any file the gate rewrites.
    "git add --all",
    # The generated project's own gate: format, check, test, and build in one task.
    "mise run all",
    # Mirrors the generated CI's "Verify no changes" step: a template file the formatters
    # would rewrite fails every new project's first push, even though `mise run all` passes.
    "git diff --exit-code",
    "mise run docs",
    "mise run project",
    "mise run build:image",
    "mise run mlflow:doctor",
]

# %% TESTS


def test_project_generation(cookies: Cookies) -> None:
    """Test the generation of the project."""
    # given
    # Toolchain versions come from cookiecutter.json, so the bake always proves the defaults users get.
    defaults = json.loads((Path(__file__).parents[1] / "cookiecutter.json").read_text(encoding="utf-8"))
    context = {
        "user": "tester",
        "name": "MLOps 123",
        "version": "1.0.0",
        "year": "2026",
        "description": "A test project.",
        "python_version": defaults["python_version"],
        "mlflow_version": defaults["mlflow_version"],
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
        "version": context["version"],
        "year": context["year"],
        "description": context["description"],
        "python_version": context["python_version"],
        "mlflow_version": context["mlflow_version"],
        # cookiecutter keeps private keys in the rendered context.
        "_copy_without_render": ["cliff.toml"],
    }
    # - commands
    # Run as a user would in a fresh checkout: `uv run pytest` exports this harness's
    # VIRTUAL_ENV, which uv in the generated project would warn about and ignore. The
    # bake lives in a temporary directory, usually on another filesystem than the uv
    # cache, so copy instead of failing to hardlink and warning on every sync.
    environ = EnvironDict({key: value for key, value in os.environ.items() if key != "VIRTUAL_ENV"})
    environ["UV_LINK_MODE"] = "copy"
    shell = Subprocess(cwd=result.project_path, environ=environ)
    for command in COMMANDS:
        result = shell.run(*command.split())
        assert result.returncode == 0, f"Command failed: {command}"
