# run package tasks
[group('package')]
package: package-build

# build package constraints
[group('package')]
package-constraints constraints="constraints.txt":
	{% raw %}uv pip compile pyproject.toml --generate-hashes --output-file={{constraints}}{% endraw %}

# build python package
[group('package')]
package-build constraints="constraints.txt": clean-build package-constraints
	{% raw %}uv build --build-constraint={{constraints}} --require-hashes --wheel{% endraw %}
