"""Scripts of the project."""

# %% IMPORTS

import sys

# %% FUNCTIONS


def main(argv: list[str] | None = None) -> int:
    """Run the main script function."""
    args = argv or sys.argv[1:]
    print("Args:", args)
    return 0
