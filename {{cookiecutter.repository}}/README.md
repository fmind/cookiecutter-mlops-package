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
- `mise run project` — invoke the MLflow CLI scaffolds; `mise run project:run <name>` runs one (`confs/<name>.yaml`).
- `mise tasks` — list everything else.

## MLflow

Tracking and the model registry use a local SQLite database (`sqlite:///mlflow.db`). The legacy file store is in maintenance mode and disabled by default in the supported MLflow version. Artifacts stay on disk.

```bash
mise run mlflow:serve   # browse runs at http://127.0.0.1:5000
mise run docker:compose # or run the same server in a container
```

Copy `.env.example` to `.env` and point `MLFLOW_TRACKING_URI` at a real database (PostgreSQL, MySQL) or a tracking server to share runs across a team — no code changes required.

## GitHub setup

- **Branch protection**: `mise run install:rulesets` applies `.github/rulesets/main.json`. It requires the `checks` status check, which is the job name in `ci.yml`; rename both or neither. The task is idempotent — re-running it updates the existing ruleset instead of creating a duplicate.
- **Documentation hosting**: go to **Settings → Pages** and set **Source** to **GitHub Actions**. The release workflow runs the complete gate, scans a candidate image by immutable digest before assigning release tags, and deploys docs through the `github-pages` environment with `actions/deploy-pages`; it does not push to a `gh-pages` branch, so it needs no write permission on the repository contents.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit). See [`LICENSE.txt`](LICENSE.txt) for details.

# Scaffold boundary

The generated CLI accepts and logs configuration paths; it does not load data, train a model, or run the YAML jobs yet. Implement that logic in `src/<package>/scripts.py`, using [mlops-python-package](https://github.com/fmind/mlops-python-package) as the working example. The bake test proves generation, the CLI, MLflow Projects invocation, documentation, and build integration. It does not certify model training or deployment.

Start the local tracking server with `mise run docker:compose`, which initializes SQLite first. Before using `docker compose up` directly, run `mise run mlflow:db`.

`mise run clean` removes caches and build outputs while preserving MLflow databases, run artifacts, and predictions. Back up experiment state before any deliberate manual reset.

The runtime image contains the installed package and locked dependencies, with pip and its bootstrap wheels removed. Rebuild the image to change dependencies.

When implementing the model workflow, follow the reference package’s `PipelineJob`: pass selected parameters into training, evaluate its exact registered version, and promote only after thresholds pass. Keep prediction schemas limited to features available at serving time. The generated task remains a CLI scaffold until this logic is implemented.
