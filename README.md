# Cookiecutter - MLOps Package

[![Release](https://img.shields.io/github/v/release/fmind/cookiecutter-mlops-package)](https://github.com/fmind/cookiecutter-mlops-package/releases) [![License](https://img.shields.io/github/license/fmind/cookiecutter-mlops-package)](https://github.com/fmind/cookiecutter-mlops-package/blob/main/LICENSE.txt)

**Jumpstart your MLOps projects with this comprehensive [Cookiecutter template](https://cookiecutter.readthedocs.io/)**.

The template provides a robust foundation for building, testing, packaging, and deploying Python packages and Docker images tailored for MLOps tasks.

**Related resources**:

- **[MLOps Coding Course (Learning)](https://mlops-coding-course.fmind.dev/)**: Learn how to create, develop, and maintain a state-of-the-art MLOps code base.
- **[MLOps Python Package (Example)](https://github.com/fmind/mlops-python-package)**: Kickstart your MLOps initiative with a flexible, robust, and productive Python package.
- **[LLMOps Coding Package (Example)](https://github.com/callmesora/llmops-python-package/)**: Example with best practices and tools to support your LLMOps projects.
- **[Agent Skills (Resource)](https://github.com/MLOps-Courses/mlops-coding-skills)**: Enhance your AI Agents with standardized skills for MLOps and coding.

## Philosophy

This [Cookiecutter](https://cookiecutter.readthedocs.io/) is designed to be a common ground for diverse MLOps environments. Whether you're working with [Kubernetes](https://www.kubeflow.org/), [Vertex AI](https://cloud.google.com/vertex-ai), [Databricks](https://www.databricks.com/), [Azure ML](https://azure.microsoft.com/en-us/products/machine-learning), or [AWS SageMaker](https://aws.amazon.com/sagemaker/), the core principles of using Python packages and Docker images remain consistent.

This template equips you with the essentials for creating, testing, and packaging your AI/ML code, providing a solid base for [integration into your chosen MLOps platform](https://fmind.medium.com/stop-building-rigid-ai-ml-pipelines-embrace-reusable-components-for-flexible-mlops-6e165d837110). To fully leverage its capabilities within a specific environment, you might need to combine it with external tools like [Airflow](https://airflow.apache.org/) for orchestration or platform-specific SDKs for deployment.

You have the freedom to structure your `src/` and `tests/` directories according to your preferences. Alternatively, you can draw inspiration from the structure used in the [MLOps Python Package](https://github.com/fmind/mlops-python-package) project for a ready-made implementation.

## Key Features

- **One task vocabulary**: [mise](https://mise.jdx.dev/) defines `install`, `format`, `check`, `test`, `build`, and the `all` gate. Git hooks, CI, and you run the exact same commands — there is no second definition to keep in sync.
- **Fast, single-tool Python stack**: [uv](https://docs.astral.sh/uv/) for dependencies and packaging, [Ruff](https://docs.astral.sh/ruff/) for linting and formatting (its `S`/bandit rules replace a separate security linter), and [ty](https://github.com/astral-sh/ty) for type checking.
- **Security in the gate, not beside it**: [pip-audit](https://pypi.org/project/pip-audit/) for dependency CVEs, [gitleaks](https://github.com/gitleaks/gitleaks) for secrets, [Trivy](https://trivy.dev/) for the whole checkout, [hadolint](https://github.com/hadolint/hadolint) for the image, and [actionlint](https://github.com/rhysd/actionlint) + [zizmor](https://docs.zizmor.sh/) for the workflows.
- **Tested by generation, not by inspection**: `mise run test` bakes a real project into a temporary directory and runs that project's own gate — format, check, test, build, docs, Docker image, and MLflow jobs.
- **MLflow on a real store**: tracking and the model registry use a SQLite database (`sqlite:///mlflow.db`), the SQLAlchemy backend MLflow 3 defaults to and the only local store the model registry was designed for.
- **Container and CI/CD included**: a multi-stage, non-root [Docker](https://www.docker.com/) image, plus [GitHub Actions](https://github.com/features/actions) workflows for the gate (`ci.yml`), the release (`cd.yml`: [pdoc](https://pdoc.dev/) docs to GitHub Pages and the image to GHCR), and a weekly full-history security rescan (`security.yml`).
- **Maintained by default**: [Dependabot](https://docs.github.com/en/code-security/dependabot) groups minor and patch bumps per ecosystem, [lefthook](https://lefthook.dev/) runs the gate before every commit and push, and [git-cliff](https://git-cliff.org/) turns Conventional Commits into a changelog.

## Quick Start

1. **Generate your project:**

```bash
uvx cookiecutter gh:fmind/cookiecutter-mlops-package
```

You'll be prompted for the following variables:

- `user`: Your GitHub username.
- `name`: The name of your project.
- `repository`: The name of your GitHub repository.
- `package`: The name of your Python package.
- `version`: The initial version of your project.
- `year`: The copyright year written into `LICENSE.txt`.
- `description`: A brief description of your project.
- `python_version`: The Python version to use (e.g., 3.14). It drives `requires-python`, the Ruff target, the ty environment, and the Docker base image at once.
- `mlflow_version`: The MLflow version to use (e.g., 3.16.1).

The generated project is MIT-licensed. To use another license, replace `LICENSE.txt` and the `license` field in `pyproject.toml` — the template does not ship alternative license texts, so there is no prompt for it.

2. **Set the project up:**

```bash
cd <your-repository>
git init          # git hooks (lefthook) and secret scanning (gitleaks) need a repository
mise install      # download the pinned toolchain (tasks never auto-install it)
mise run install  # sync the virtualenv (uv) and install git hooks (lefthook)
```

3. **Configure the GitHub repository:**

- **Documentation hosting**: go to **Settings → Pages** and set **Source** to **GitHub Actions**. The shipped `cd.yml` deploys through the `github-pages` environment with `actions/deploy-pages`; it never pushes to a branch, so it does not need "Read and write permissions" under Actions.
- **Branch protection**: run `mise run install:rulesets` to apply `.github/rulesets/main.json`. It requires the `checks` status check, which is the `ci.yml` job name; rename both or neither.

4. **Explore the generated project:**

- `src/<your-package>/`: your Python package source code.
- `tests/`: the `pytest` suite, with coverage enforced by `mise run test`.
- `confs/`: one config file per MLflow job.
- `Dockerfile` / `docker-compose.yml`: the production image and a local MLflow server.
- `mise.toml`: every task; `mise tasks` lists them.

5. **Start developing:**

```bash
mise run all      # the gate: format, check, test, build
mise run project  # run every MLflow job
mise tasks        # list everything else
```

## Working on the Template

This repository has two layers, each with its own toolchain: the harness at the root (a [pytest-cookies](https://github.com/hackebrot/pytest-cookies) bake suite) and the template sources under `{{cookiecutter.repository}}/`.

```bash
mise install      # download the pinned toolchain
mise run install  # sync the virtualenv and install git hooks
mise run all      # format, check, and test the harness
```

`mise run test` is the real proof: it bakes a project into a temporary directory and runs the generated project's own gate inside it, including a Docker build and MLflow jobs. It takes several minutes and needs `docker` running.

Keep the template in sync with the reference implementation, [mlops-python-package](https://github.com/fmind/mlops-python-package): shared configuration files should differ only by their cookiecutter variables. See [`AGENTS.md`](AGENTS.md) for the conventions that keep both layers honest.

## Contributions

We welcome [contributions](https://github.com/fmind/cookiecutter-mlops-package/blob/main/CODE_OF_CONDUCT.md) to enhance this [Cookiecutter template](https://cookiecutter.readthedocs.io/) for generating MLOps projects.

Feel free to open [issues](https://github.com/fmind/cookiecutter-mlops-package/issues) or [pull requests](https://github.com/fmind/cookiecutter-mlops-package/pulls) for any improvements, bug fixes, or feature requests.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit). See the [`LICENSE.txt`](https://github.com/fmind/cookiecutter-mlops-package/blob/main/LICENSE.txt) file for details.
