"""Reject invalid identifiers before writing a generated project."""

import keyword
import re

package = {{ cookiecutter.package | tojson }}
repository = {{ cookiecutter.repository | tojson }}
python_version = {{ cookiecutter.python_version | tojson }}

if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", package) or keyword.iskeyword(package):
    raise SystemExit("Python package must be a valid, non-keyword identifier (for example: mlops_project).")
if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", repository):
    raise SystemExit("Repository must use lowercase letters, digits, and single hyphens (for example: mlops-project).")
if not re.fullmatch(r"3\.[0-9]+", python_version):
    raise SystemExit("Python version must be a major.minor value (for example: 3.14).")

# TOML supports escaped whitespace, but rejects other control characters.
for value in [{{ cookiecutter.description | tojson }}, {{ cookiecutter.user | tojson }}, {{ cookiecutter.version | tojson }}]:
    if any(ord(char) < 32 and char not in "\b\t\n\f\r" for char in value):
        raise SystemExit("Metadata must not contain unsupported control characters.")
