# AGENTS.md

Context and rules for AI agents working in this repository. Humans should start with `README.md`.

## Project overview

- **Name**: cookiecutter-mlops-package — a [Cookiecutter](https://cookiecutter.readthedocs.io/) template that scaffolds MLOps Python packages.
- **Layout**: `{{cookiecutter.repository}}/` holds the template sources (raw Jinja); `tests/test_cookiecutter.py` bakes the template and runs the generated project's full toolchain.
- **Language**: Python 3.14+ (`pyproject.toml`), managed with `uv`.
- **Reference**: [mlops-python-package](https://github.com/fmind/mlops-python-package) is the reference implementation. Shared configuration files should differ from it only by cookiecutter variables; diff against it before changing the template.

## Setup & core commands

All work goes through `mise` (see `mise.toml`); git hooks (`lefthook.yml`) and CI call the same tasks.

- Everything: `mise run all` — format, check, test. This is the gate; CI runs this exact task and nothing else. There is no `build` step: `[tool.uv] package = false`, this repository is a test suite, not a distribution.
- Install: `mise install` provisions the pinned toolchain (`run_auto_install` is off), then `mise run install` syncs the virtualenv (`uv sync`) and installs git hooks.
- Format: `mise run format` — `ruff` (import sort + format, including Python inside Markdown) and `dprint` (JSON/Markdown/TOML/YAML).
- Check: `mise run check` — `ruff` lint, `ty` types, `pip-audit` deps, `dprint`/`validate-pyproject`/`uv lock` format, `gitleaks` secrets, `trivy` filesystem scan, `actionlint` + `zizmor` workflows.
- Test: `mise run test` — `pytest` bakes the template and runs `mise trust`/`mise install`/`git init`/`mise run all`/... inside the generated project. Needs `docker` running and takes several minutes.

## Definition of done

A change is complete only when, locally, `mise run all` passes warning-free — which includes the bake test actually generating a project and passing that project's own gate. Fix root causes — never weaken an assertion, add a skip/`xfail`, loosen a type, or suppress a lint error to force a green result.

## Conventions & idioms

- **Two toolchains**: the harness (this repo root) and the generated project (`{{cookiecutter.repository}}/`) each have their own `mise.toml`/`pyproject.toml`/`lefthook.yml`/`dprint.jsonc`/`trivy.yaml`. A change to one usually belongs in both; the exceptions are things the harness does not have (a `Dockerfile`, a `src/`, a distribution to build, a `docker` Dependabot ecosystem).
- **Change the template, not the bake output**: the bake writes to a temporary directory. Editing a generated project proves nothing and is thrown away.
- **Jinja templating**: GitHub Actions expressions `${{ ... }}` inside `{{cookiecutter.repository}}/.github/workflows/*.yml` must be wrapped in `{% raw %}...{% endraw %}` so cookiecutter does not render them — including inside YAML comments, where a bare `${{ }}` is still a Jinja expression and will fail the bake.
- **One answer, one fact**: `{{cookiecutter.python_version}}` drives `requires-python`, `[tool.ruff] target-version` (via `.replace('.', '')`), `[tool.ty.environment]`, `.python-version`, and the `Dockerfile` base image. Never hardcode a value that a variable already carries.
- **Status check name**: the template's `ci.yml` job is `checks` because `{{cookiecutter.repository}}/.github/rulesets/main.json` requires that context. Renaming one without the other blocks every pull request in every generated project on a check that can never report.
- **Excludes**: `dprint`, `ruff`, and `ty` skip `{{cookiecutter.repository}}/` at the root because raw Jinja is not valid JSON/YAML/TOML/Python. `actionlint` and `zizmor` only see this repository's own `.github/workflows`; the template's workflows are linted inside the baked project.
- **Prompts earn their keep**: every key in `cookiecutter.json` must be consumed by a rendered file. A prompt nothing reads is a lie to the user — delete it or wire it up.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `chore:`); no attribution in commit messages. Releases use `git-cliff` (see `cliff.toml`).

## Repository layout

- `{{cookiecutter.repository}}/` — the generated project template (own `mise.toml`, `pyproject.toml`, `src/`, `tests/`, `confs/`, `Dockerfile`, `.github/`).
- `cookiecutter.json` — template variables, defaults, and prompts; `tests/test_cookiecutter.py` — the bake-and-run integration test and the list of commands it runs in the generated project.
- `pyproject.toml` — harness dependencies and `ruff`/`ty`/`pytest` config; `mise.toml`/`mise.lock` — tasks and pinned, locked tools; `lefthook.yml` — git hooks; `dprint.jsonc`/`trivy.yaml`/`cliff.toml` — formatter, scanner, changelog config.
- `.github/` — `workflows/` (`ci.yml` runs `mise run all`, `security.yml` rescans the full history weekly), `dependabot.yml`, `zizmor.yml`.
