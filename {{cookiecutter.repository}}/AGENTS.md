# AGENTS.md

Context and rules for AI agents working in this repository. Humans should start with `README.md`.

## Project overview

- **Name**: {{cookiecutter.repository}} — {{cookiecutter.description}}
- **Description**: MLOps package generated from [cookiecutter-mlops-package](https://github.com/fmind/cookiecutter-mlops-package).
- **Language**: Python {{cookiecutter.python_version}}+ (`pyproject.toml`), managed with `uv`.
- **Stack**: MLflow (tracking, registry, projects) as the backbone; extend `src/{{cookiecutter.package}}/` with your own logic.

## Setup & core commands

All work goes through `mise` (see `mise.toml`); git hooks (`lefthook.yml`) and CI call the same tasks.

- Everything: `mise run all` — format, check, test, build. This is the gate; CI runs this exact task and nothing else.
- Install: `mise run install` — sync the virtualenv (`uv sync`) and install git hooks. Run `mise install` first to provision the pinned toolchain (`run_auto_install` is off on purpose, so a task never installs a tool behind your back).
- Format: `mise run format` — `ruff` (import sort + format, including Python inside Markdown) and `dprint` (JSON/Markdown/TOML/YAML).
- Check: `mise run check` — `ruff` lint, `ty` types, `pip-audit` deps, `dprint`/`validate-pyproject`/`uv lock` format, `gitleaks` secrets, `trivy` filesystem scan, `hadolint` Dockerfile, `actionlint` + `zizmor` workflows.
- Test: `mise run test` — `pytest` with coverage; `mise run test:parallel` is a faster, coverage-free local loop.
- Build: `mise run build` — `uv build` (wheel + sdist); `mise run build:image` builds the Docker image.
- Docs: `mise run docs` — `pdoc` API reference into `docs/`.
- MLflow jobs: `mise run project` runs every job; `mise run project:run <name>` runs one (`confs/<name>.yaml`).

## Definition of done

A change is complete only when, locally, `mise run all` passes warning-free and new/changed behavior is covered by a test. Fix root causes — never weaken an assertion, add a skip/`xfail`, loosen a type, or suppress a lint error to force a green result.

## Conventions & idioms

- **Errors with context**: raise specific exceptions and chain with `raise ... from err`; never use a bare `except` or silently swallow errors.
- **Typing**: modern annotations (`list[str]`, `X | Y`); keep `ty check` clean. `import typing as T` is the project convention.
- **Logging**: `loguru`; no bare prints in library code.
- **MLflow**: tracking and registry run on a SQLite backend (`sqlite:///mlflow.db`, the same store MLflow 3 now defaults to); artifact files stay on disk under `./mlruns`, and the standalone server in `docker-compose.yml` writes artifacts to `./mlartifacts`. This is the same SQLAlchemy store shape as a production PostgreSQL and the store the model registry is designed for, so moving up is an `MLFLOW_TRACKING_URI` change (see `.env.example`), not a rewrite.
- **Coverage**: the gate starts at 80% (`--cov-fail-under` in `pyproject.toml`) because a fresh package has little to cover. Raise it as the suite grows; never lower it to make a run pass.
- **Python version**: `{{cookiecutter.python_version}}` is set once by the template and reused by `requires-python`, `[tool.ruff] target-version`, `[tool.ty.environment]`, `.python-version`, and the `Dockerfile` base image. Change all of them together.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `chore:`); no attribution in commit messages. Releases use `git-cliff` (see `cliff.toml`).

## Repository layout

- `src/{{cookiecutter.package}}/` — package: `scripts.py` (CLI entry point), `__main__.py`, `__init__.py`. Add `core/`, `io/`, `jobs/`, `utils/` modules as the project grows.
- `confs/` — one config file per MLflow job; `tests/` — `pytest` suite mirroring `src/` with fixtures in `conftest.py`.
- `pyproject.toml` — dependencies and `ruff`/`ty`/`pytest` config; `mise.toml` — tasks and pinned tools; `lefthook.yml` — git hooks; `dprint.jsonc`/`trivy.yaml`/`cliff.toml` — formatter, scanner, changelog config.
- `.github/` — `workflows/` (`ci.yml` runs `mise run all`, `cd.yml` publishes docs and the image, `security.yml` rescans the full history weekly), `dependabot.yml`, `zizmor.yml`, `rulesets/main.json`. The `ci.yml` job is named `checks` because `rulesets/main.json` requires that status check context; rename both or neither.
- `Dockerfile`/`docker-compose.yml`/`MLproject` — container image, local MLflow server, and MLflow Projects reproducible runs (`--env-manager=local` reuses the uv environment, so there is no `python_env.yaml`).
