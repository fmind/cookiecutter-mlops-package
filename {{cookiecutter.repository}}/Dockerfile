# https://docs.docker.com/engine/reference/builder/

FROM ghcr.io/astral-sh/uv:python{{cookiecutter.python_version}}-bookworm
COPY dist/*.whl .
RUN uv pip install --system *.whl
CMD ["{{cookiecutter.repository}}", "--help"]
