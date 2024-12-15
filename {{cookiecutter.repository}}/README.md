# {{cookiecutter.name}}

[![check.yml](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/check.yml/badge.svg)](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/check.yml)
[![publish.yml](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/publish.yml/badge.svg)](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/actions/workflows/publish.yml)
[![Documentation](https://img.shields.io/badge/documentation-available-brightgreen.svg)](https://{{cookiecutter.user}}.github.io/{{cookiecutter.repository}}/)
[![License](https://img.shields.io/github/license/{{cookiecutter.user}}/{{cookiecutter.repository}})](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/blob/main/LICENCE.txt)
[![Release](https://img.shields.io/github/v/release/{{cookiecutter.user}}/{{cookiecutter.repository}})](https://github.com/{{cookiecutter.user}}/{{cookiecutter.repository}}/releases)

{{cookiecutter.description}}.

# Installation

Use the package manager [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

# Usage

```bash
uv run {{cookiecutter.repository}}
```
