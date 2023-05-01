"""Main entrypoint for package."""
from .cli import minelog_cli

if __name__ == "__main__":
    minelog_cli()  # pylint: disable=no-value-for-parameter,missing-kwoa
