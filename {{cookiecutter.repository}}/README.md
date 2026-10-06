# {{cookiecutter.name}}

[![ci.yml](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/ci.yml) [![cd.yml](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/cd.yml/badge.svg)](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/cd.yml) [![Documentation](https://img.shields.io/badge/documentation-available-brightgreen.svg)](https://{{cookiecutter.user}}.github.io/{{cookiecutter.repository}}/) [![License](https://img.shields.io/github/license/{{cookiecutter.user}}/{{cookiecutter.repository}})](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/blob/main/LICENSE.txt) [![Release](https://img.shields.io/github/v/release/{{cookiecutter.user}}/{{cookiecutter.repository}})](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/releases)

{{cookiecutter.description}}

## Installation

This project uses [mise](https://mise.jdx.dev/) to expose a common task vocabulary and pin its toolchain (`uv`, `dprint`, `gitleaks`, `trivy`, `hadolint`, `actionlint`, `zizmor`, `git-cliff`). Install [mise](https://mise.jdx.dev/getting-started.html), then:

```bash
git init          # git hooks (lefthook) and secret scanning (gitleaks) need a repository
mise install      # download the pinned toolchain (tasks never auto-install it)
mise run install  # sync the virtualenv (uv) and install git hooks (lefthook)
```

`mise.toml` pins every tool to an exact version and `mise.lock` records their checksums, so every install is verified. After changing a pin, refresh the lock and commit both:

```bash
mise lock
```

## Usage

```bash
uv run {{cookiecutter.repository}} confs/training.yaml
```

## Tasks

All work goes through `mise`; git hooks (`lefthook.yml`) and CI run the same tasks.

- `mise run all` — the canonical gate: format, check, test, build. CI runs this task and nothing else.
- `mise run format` — format Python (`ruff`) and config/markup files (`dprint`).
- `mise run check` — lint (`ruff`), type-check (`ty`), audit dependencies (`pip-audit`), scan the checkout (`gitleaks`, `trivy`), lint the `Dockerfile` (`hadolint`) and the workflows (`actionlint`, `zizmor`).
- `mise run test` — run the test suite with coverage (`pytest`); `mise run test:parallel` skips the coverage gate for a faster loop.
- `mise run build` — build the wheel + sdist (`uv build`); `mise run build:image` builds the Docker image.
- `mise run docs` — generate the API documentation (`pdoc`).
- `mise run project` — run every MLflow job; `mise run project:run <name>` runs one (`confs/<name>.yaml`).
- `mise tasks` — list everything else.

## MLflow

Tracking and the model registry run on a local SQLite database (`sqlite:///mlflow.db`), which is what MLflow 3 defaults to and the only local store the model registry was designed for. Artifacts stay on disk.

```bash
mise run mlflow:serve   # browse runs at http://127.0.0.1:5000
mise run docker:compose # or run the same server in a container
```

Copy `.env.example` to `.env` and point `MLFLOW_TRACKING_URI` at a real database (PostgreSQL, MySQL) or a tracking server to share runs across a team — no code changes required.

## GitHub setup

- **Branch protection**: `mise run install:rulesets` applies `.github/rulesets/main.json`. It requires the `checks` status check, which is the job name in `ci.yml`; rename both or neither. The task is idempotent — re-running it updates the existing ruleset instead of creating a duplicate.
- **Documentation hosting**: go to **Settings → Pages** and set **Source** to **GitHub Actions**. `cd.yml` deploys through the `github-pages` environment with `actions/deploy-pages`; it does not push to a `gh-pages` branch, so it needs no write permission on the repository contents.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit). See [`LICENSE.txt`](LICENSE.txt) for details.
