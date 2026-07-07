"""Scripts for the CLI application."""

# %% IMPORTS

import argparse

from loguru import logger

# %% PARSERS

parser = argparse.ArgumentParser(description="Run an AI/ML job from YAML/JSON configs.")
parser.add_argument("files", nargs="*", help="Config files for the job (local paths only).")

# %% SCRIPTS


def main(argv: list[str] | None = None) -> int:
    """Run the main script of the application.

    Args:
        argv: optional list of command-line arguments (defaults to `sys.argv`).

    Returns:
        The exit code of the application (0 on success).
    """
    args = parser.parse_args(argv)
    logger.info("Running job with configs: {}", args.files)
    return 0
