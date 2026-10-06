"""Test that each layer's mise.lock matches its mise.toml pins."""

# %% IMPORTS

import tomllib
from pathlib import Path

import pytest

# %% CONFIGS

ROOT = Path(__file__).parents[1]

# %% TESTS


# The template's lock ships to every generated project, and nothing else would notice it
# going stale: mise silently re-resolves a mismatched entry instead of failing.
@pytest.mark.parametrize("layer", [ROOT, ROOT / "{{cookiecutter.repository}}"], ids=["harness", "template"])
def test_lock_matches_pins(layer: Path) -> None:
    # given
    pins = tomllib.loads((layer / "mise.toml").read_text(encoding="utf-8"))["tools"]
    lock = tomllib.loads((layer / "mise.lock").read_text(encoding="utf-8"))["tools"]
    # when
    locked = {tool: [entry["version"] for entry in entries] for tool, entries in lock.items()}
    # then
    assert locked == {tool: [version] for tool, version in pins.items()}, (
        f"Run `mise lock` in {layer.name} after changing a pin."
    )
