# run format tasks
[group('format')]
format: format-import format-source

# format code import
[group('format')]
format-import:
    {% raw %}uv run ruff check --select=I --fix {{SOURCES}} {{TESTS}}{% endraw %}

# format code source
[group('format')]
format-source:
    {% raw %}uv run ruff format {{SOURCES}} {{TESTS}}{% endraw %}
