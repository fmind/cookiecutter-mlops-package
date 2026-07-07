# AGENTS.md

Context and rules for AI agents working in this repository. Humans should start with `README.md`.

## Project overview

- **Name**: cookiecutter-mlops-package — a [Cookiecutter](https://cookiecutter.readthedocs.io/) template that scaffolds MLOps Python packages.
- **Layout**: `{{cookiecutter.repository}}/` holds the template sources (raw Jinja); `tests/test_cookiecutter.py` bakes the template and runs the generated project's full toolchain.
- **Language**: Python 3.14+ (`pyproject.toml`), managed with `uv`.

## Setup & core commands

All work goes through `mise` (see `mise.toml`); git hooks (`lefthook.yml`) and CI call the same tasks.

- Install: `mise run install` — sync the virtualenv (`uv sync`) and install git hooks.
- Format: `mise run format` — `ruff` (import sort + format) and `dprint` (JSON/Markdown/TOML/YAML).
- Check: `mise run check` — `ruff` lint, `ty` types, `pip-audit` deps, `dprint`/`validate-pyproject`/`uv lock` format, `gitleaks` secrets, `trivy` config.
- Test: `mise run test` — `pytest` bakes the template and runs `mise trust`/`git init`/`mise run ...` inside the generated project (Docker + MLflow required).

## Definition of done

A change is complete only when, locally, `mise run format` is clean, `mise run check` reports no findings, and `mise run test` is green. Fix root causes — never weaken an assertion, add a skip/`xfail`, loosen a type, or suppress a lint error to force a green result.

## Conventions & idioms

- **Two toolchains**: the harness (this repo root) and the generated project (`{{cookiecutter.repository}}/`) each have their own `mise.toml`/`pyproject.toml`. Keep the template in sync with the reference package `mlops-python-package`, using cookiecutter variables.
- **Jinja templating**: GitHub Actions expressions `${{ ... }}` inside `{{cookiecutter.repository}}/.github/workflows/*.yml` must be wrapped in `{% raw %}...{% endraw %}` so cookiecutter does not render them.
- **Excludes**: `dprint`, `ruff`, and `ty` skip `{{cookiecutter.repository}}/` at the root because raw Jinja is not valid JSON/YAML/TOML/Python.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `chore:`); no attribution in commit messages. Releases use `git-cliff` (see `cliff.toml`).

## Repository layout

- `{{cookiecutter.repository}}/` — the generated project template (own `mise.toml`, `pyproject.toml`, `src/`, `tests/`, `confs/`, `Dockerfile`, workflows).
- `cookiecutter.json` — template variables and defaults; `tests/test_cookiecutter.py` — the bake-and-run integration test.
- `pyproject.toml` — harness dependencies and `ruff`/`ty` config; `mise.toml` — tasks and pinned tools; `lefthook.yml` — git hooks; `dprint.jsonc`/`trivy.yaml`/`cliff.toml` — formatter, scanner, changelog config.
