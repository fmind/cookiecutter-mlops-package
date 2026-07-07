# AGENTS.md

Context and rules for AI agents working in this repository. Humans should start with `README.md`.

## Project overview

- **Name**: {{cookiecutter.repository}} — {{cookiecutter.description}}
- **Description**: MLOps package generated from [cookiecutter-mlops-package](https://github.com/fmind/cookiecutter-mlops-package).
- **Language**: Python {{cookiecutter.python_version}}+ (`pyproject.toml`), managed with `uv`.
- **Stack**: MLflow (tracking, registry, projects) as the backbone; extend `src/{{cookiecutter.package}}/` with your own logic.

## Setup & core commands

All work goes through `mise` (see `mise.toml`); git hooks (`lefthook.yml`) and CI call the same tasks.

- Install: `mise run install` — sync the virtualenv (`uv sync`) and install git hooks.
- Format: `mise run format` — `ruff` (import sort + format) and `dprint` (JSON/Markdown/TOML/YAML).
- Check: `mise run check` — `ruff` lint, `ty` types, `pip-audit` deps, `dprint`/`validate-pyproject`/`uv lock` format, `gitleaks` secrets, `trivy` config.
- Test: `mise run test` — `pytest` with coverage.
- Build: `mise run build` — `uv build` (wheel + sdist); `mise run build:image` builds the Docker image.
- Docs: `mise run docs` — `pdoc` API reference into `docs/`.
- MLflow jobs: `mise run project` runs every job; `mise run project:run <name>` runs one (`confs/<name>.yaml`).

## Definition of done

A change is complete only when, locally, `mise run format` is clean, `mise run check` reports no findings, and `mise run test` is green with new/changed behavior covered by a test. Fix root causes — never weaken an assertion, add a skip/`xfail`, loosen a type, or suppress a lint error to force a green result.

## Conventions & idioms

- **Errors with context**: raise specific exceptions and chain with `raise ... from err`; never use a bare `except` or silently swallow errors.
- **Typing**: modern annotations (`list[str]`, `X | Y`); keep `ty check` clean. `import typing as T` is the project convention.
- **Logging**: `loguru`; no bare prints in library code.
- **MLflow**: the file store (`./mlruns`) is opted in via `MLFLOW_ALLOW_FILE_STORE` for local development; prefer a database backend in production.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `chore:`); no attribution in commit messages. Releases use `git-cliff` (see `cliff.toml`).

## Repository layout

- `src/{{cookiecutter.package}}/` — package: `scripts.py` (CLI entry point), `__main__.py`, `__init__.py`. Add `core/`, `io/`, `jobs/`, `utils/` modules as the project grows.
- `confs/` — one config file per MLflow job; `tests/` — `pytest` suite mirroring `src/` with fixtures in `conftest.py`.
- `pyproject.toml` — dependencies and `ruff`/`ty`/`pytest` config; `mise.toml` — tasks and pinned tools; `lefthook.yml` — git hooks; `dprint.jsonc`/`trivy.yaml`/`cliff.toml` — formatter, scanner, changelog config.
- `Dockerfile`/`docker-compose.yml`/`MLproject` — container image, local MLflow server, and MLflow Projects reproducible runs.
