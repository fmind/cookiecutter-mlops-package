# Cookiecutter - MLOps Package

[![Release](https://img.shields.io/github/v/release/fmind/cookiecutter-mlops-package)](https://github.com/fmind/cookiecutter-mlops-package/releases)
[![License](https://img.shields.io/github/license/fmind/cookiecutter-mlops-package)](https://github.com/fmind/cookiecutter-mlops-package/blob/main/LICENSE.txt)

**Jumpstart your MLOps projects with this comprehensive [Cookiecutter template](https://cookiecutter.readthedocs.io/)**.

The template provides a robust foundation for building, testing, packaging, and deploying Python packages and Docker Images tailored for MLOps tasks.

**Related resources**:
- **[MLOps Coding Course (Learning)](https://mlops-coding-course.fmind.dev/)**: Learn how to create, develop, and maintain a state-of-the-art MLOps code base.
- **[MLOps Python Package (Example)](https://github.com/fmind/mlops-python-package)**: Kickstart your MLOps initiative with a flexible, robust, and productive Python package.
- **[LLMOps Coding Package (Example)](https://github.com/callmesora/llmops-python-package/)**: Example with best practices and tools to support your LLMOps projects.

## Philosophy

This [Cookiecutter](https://cookiecutter.readthedocs.io/) is designed to be a common ground for diverse MLOps environments. Whether you're working with [Kubernetes](https://www.kubeflow.org/), [Vertex AI](https://cloud.google.com/vertex-ai), [Databricks](https://www.databricks.com/), [Azure ML](https://azure.microsoft.com/en-us/products/machine-learning), or [AWS SageMaker](https://aws.amazon.com/sagemaker/), the core principles of using Python packages and Docker images remain consistent.

This template equips you with the essentials for creating, testing, and packaging your AI/ML code, providing a solid base for integration into your chosen MLOps platform. To fully leverage its capabilities within a specific environment, you might need to combine it with external tools like [Airflow](https://airflow.apache.org/) for orchestration or platform-specific SDKs for deployment.

You have the freedom to structure your `src/` and `tests/` directories according to your preferences. Alternatively, you can draw inspiration from the structure used in the [MLOps Python Package](https://github.com/fmind/mlops-python-package) project for a ready-made implementation.

## Key Features

* **Streamlined Project Structure:** A well-defined directory layout for source code, tests, documentation, tasks, and Docker configurations.
* **Uv Integration:** Effortless dependency management and packaging with [uv](https://docs.astral.sh/uv/).
* **Automated Testing and Checks:** Pre-configured workflows using [Pytest](https://docs.pytest.org/), [Ruff](https://docs.astral.sh/ruff/), [Mypy](https://mypy.readthedocs.io/), [Bandit](https://bandit.readthedocs.io/), and [Coverage](https://coverage.readthedocs.io/) to ensure code quality, style, security, and type safety.
* **Pre-commit Hooks:** Automatic code formatting and linting with [Ruff](https://docs.astral.sh/ruff/) and other pre-commit hooks to maintain consistency.
* **Dockerized Deployment:** Dockerfile and docker-compose.yml for building and running the package within a containerized environment ([Docker](https://www.docker.com/)).
* **Invoke Task Automation:** [PyInvoke](https://www.pyinvoke.org/) tasks to simplify development workflows such as cleaning, installing, formatting, checking, building, documenting, and running MLflow projects.
* **Comprehensive Documentation:** [pdoc](https://pdoc.dev/) generates API documentation, and Markdown files provide clear usage instructions.
* **GitHub Workflow Integration:** Continuous integration and deployment workflows are set up using [GitHub Actions](https://github.com/features/actions), automating testing, checks, and publishing.


## Quick Start

1. **Generate your project:**

```bash
pip install cookiecutter
cookiecutter gh:fmind/cookiecutter-mlops-package
```

You'll be prompted for the following variables:

- `user`: Your GitHub username.
- `name`: The name of your project.
- `repository`: The name of your GitHub repository.
- `package`: The name of your Python package.
- `license`: The license for your project.
- `version`: The initial version of your project.
- `description`: A brief description of your project.
- `python_version`: The Python version to use (e.g., 3.12).
- `mlflow_version`: The MLflow version to use (e.g., 2.19.0).

2. **Initialize a git repository:**

```bash
cd {{ cookiecutter.repository }}
git init
```

3. **Enable GitHub Pages Workflow:**

- Navigate to your repository settings on GitHub: "Settings" -> "Actions" -> "General."
- Under "Workflow permissions," ensure "Read and write permissions" is selected.
    - This allows the workflow to automatically publish your documentation.

4. **Explore the generated project:**

- `src/{{cookiecutter.package}}`: Your Python package source code.
- `tests/`: Unit tests for your package.
- `tasks/`: PyInvoke tasks for automation.
- `Dockerfile`: Configuration for building your Docker image.
- `docker-compose.yml`: Orchestration file for running MLflow and your project.

5. **Start developing!**

Use the provided Invoke tasks to manage your development workflow:

- `invoke installs`: Install dependencies and pre-commit hooks.
- `invoke formats`: Format your code.
- `invoke checks`: Run code quality, type, security, and test checks.
- `invoke docs`: Generate API documentation.
- `invoke packages`: Build your Python package.
- `invoke projects`: Run MLflow projects.
- `invoke containers`: Build and run your Docker image.

## Example Usage

### Running an MLflow Project

After installing dependencies and setting up MLflow:

```bash
invoke projects
```

This will execute the job with the configuration file in your `confs` folder.

### Building and Running Your Docker Image

```bash
invoke containers
```

This builds a Docker image based on your [`Dockerfile`](https://github.com/fmind/cookiecutter-mlops-package/blob/main/%7B%7Bcookiecutter.repository%7D%7D/Dockerfile) and runs it. The `CMD` in the Dockerfile executes your package with the `--help` flag.

## Contributions

We welcome [contributions](https://github.com/fmind/cookiecutter-mlops-package/blob/main/CODE_OF_CONDUCT.md) to enhance this [Cookiecutter template](https://cookiecutter.readthedocs.io/) for generating MLOps projects.

Feel free to open [issues](https://github.com/fmind/cookiecutter-mlops-package/issues) or [pull requests](https://github.com/fmind/cookiecutter-mlops-package/pulls) for any improvements, bug fixes, or feature requests.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit). See the [`LICENSE.txt`](https://github.com/fmind/cookiecutter-mlops-package/blob/main/LICENSE.txt) file for details.
