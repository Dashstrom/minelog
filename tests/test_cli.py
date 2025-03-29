"""Test for command line interface."""

import os
import subprocess
import sys

from click.testing import CliRunner

from minelog import minelog_cli


def test_cli_version() -> None:
    """Test if the command line interface is installed correctly."""
    name = "minelog"
    env = os.environ.get("VIRTUAL_ENV", "")
    if env:
        if os.name == "nt":
            exe = f"{env}\\\\Scripts\\\\{name}.cmd"
            if not os.path.exists(exe):  # noqa: PTH110
                exe = f"{env}\\\\Scripts\\\\{name}.exe"
        else:
            exe = f"{env}/bin/{name}"
    else:
        exe = name
    out = subprocess.check_output((exe, "--version"), text=True, shell=False)
    assert "version" in out
    out = subprocess.check_output(
        (
            sys.executable,
            "-m",
            "minelog",
            "--version",
        ),
        text=True,
        shell=False,
    )
    assert "version" in out
    runner = CliRunner()
    result = runner.invoke(minelog_cli, ["--version"])
    out = result.output
    assert "version" in out


def test_import() -> None:
    """Test if module entrypoint has correct imports."""
    import minelog.__main__  # noqa: F401
