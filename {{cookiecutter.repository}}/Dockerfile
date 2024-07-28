# https://docs.docker.com/engine/reference/builder/

FROM python:{{cookiecutter.python_version}}
COPY dist/*.whl .
RUN pip install *.whl
CMD ["{{cookiecutter.repository}}", "--help"]
