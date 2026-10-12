"""Scripts for the CLI application."""

# %% IMPORTS

import argparse

from loguru import logger

# %% PARSERS

parser = argparse.ArgumentParser(description="CLI scaffold: accepts config paths; implement your job runner here.")
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
    logger.info("Scaffold received config paths: {}. Implement job execution in main().", args.files)
    return 0
