# run check tasks
[group('check')]
check: check-code check-type check-format check-security check-coverage

# check code quality
[group('check')]
check-code:
    {% raw %}uv run ruff check {{SOURCES}} {{TESTS}}{% endraw %}

# check code coverage
[group('check')]
check-coverage numprocesses="auto" cov_fail_under="80":
    {% raw %}uv run pytest --numprocesses={{numprocesses}} --cov={{SOURCES}} --cov-fail-under={{cov_fail_under}} {{TESTS}}{% endraw %}

# check code format
[group('check')]
check-format:
    {% raw %}uv run ruff format --check {{SOURCES}} {{TESTS}}{% endraw %}

# check code security
[group('check')]
check-security:
    {% raw %}uv run bandit --recursive --configfile=pyproject.toml {{SOURCES}}{% endraw %}

# check unit tests
[group('check')]
check-test numprocesses="auto":
    {% raw %}uv run pytest --numprocesses={{numprocesses}} {{TESTS}}{% endraw %}

# check code typing
[group('check')]
check-type:
    {% raw %}uv run mypy {{SOURCES}} {{TESTS}}{% endraw %}
