# {{cookiecutter.name}}

[![ci.yml](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/ci.yml) [![cd.yml](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/cd.yml/badge.svg)](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/cd.yml) [![Documentation](https://img.shields.io/badge/documentation-available-brightgreen.svg)](https://{{cookiecutter.user}}.github.io/{{cookiecutter.repository}}/) [![License](https://img.shields.io/github/license/{{cookiecutter.user}}/{{cookiecutter.repository}})](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/blob/main/LICENSE.txt) [![Release](https://img.shields.io/github/v/release/{{cookiecutter.user}}/{{cookiecutter.repository}})](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/releases)

{{cookiecutter.description}}

## Installation

This project uses [mise](https://mise.jdx.dev/) to expose a common task vocabulary and pin its toolchain (`uv`, `dprint`, `gitleaks`, `trivy`). Install [mise](https://mise.jdx.dev/getting-started.html), then:

```bash
git init          # git hooks (lefthook) and secret scanning (gitleaks) need a repository
mise run install  # sync the virtualenv (uv) and install git hooks (lefthook)
```

## Usage

```bash
uv run {{cookiecutter.repository}} confs/training.yaml
```

## Tasks

All work goes through `mise`; git hooks (`lefthook.yml`) and CI run the same tasks.

- `mise run format` — format Python (`ruff`) and config/markup files (`dprint`).
- `mise run check` — lint (`ruff`), type-check (`ty`), audit deps (`pip-audit`), scan secrets/config (`gitleaks`, `trivy`).
- `mise run test` — run the test suite with coverage (`pytest`).
- `mise run build` — build the wheel + sdist (`uv build`); `mise run build:image` builds the Docker image.
- `mise run docs` — generate the API documentation (`pdoc`).
- `mise run project` — run every MLflow job; `mise run project:run <name>` runs one (`confs/<name>.yaml`).

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit). See [`LICENSE.txt`](LICENSE.txt) for details.
