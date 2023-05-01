"""Base module for testing command line interface."""
import subprocess
import sys

import click.testing

from minelog import __version__, minelog_cli


def test_cli() -> None:
    """Basic test for command line interface."""
    ver = f"version {__version__}"
    out = subprocess.check_output(
        ["minelog", "--version"],
        text=True,
        shell=False,
    )
    assert ver in out
    out = subprocess.check_output(
        [sys.executable, "-m", "minelog", "--version"],
        text=True,
        shell=False,
    )
    assert ver in out
    runner = click.testing.CliRunner()
    result = runner.invoke(minelog_cli, ["--version"])
    out = result.output
    assert ver in out
