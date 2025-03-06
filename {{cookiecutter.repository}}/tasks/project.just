# run project tasks
[group('project')]
project: project-requirements (project-run "tuning") (project-run "training") (project-run "inference")

# export requirements file
[group('project')]
project-requirements:
    uv export --format=requirements-txt --no-dev --no-hashes \
        --no-editable --no-emit-project --output-file=requirements.txt

# run project job with a config
[group('project')]
project-run job:
    {% raw %}uv run {{REPOSITORY}} confs/{job}.yaml{% endraw %}
