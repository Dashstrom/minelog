"""Module for use module as a cli."""
import pathlib
from typing import Optional

import click

from .core import MC_ENCODING, MineLog
from .info import __copyright__, __description__, __version__


@click.command("minelog", help=__description__, epilog=__copyright__)
@click.version_option(__version__)
@click.option(
    "-d",
    "--directory",
    metavar="DIR",
    help="Path to logs.",
    type=click.Path(  # type: ignore[type-var]
        exists=True,
        dir_okay=True,
        readable=True,
        path_type=pathlib.Path,
    ),
)
@click.option(
    "-p",
    "--pattern",
    metavar="PATTERN",
    help="Pattern used for search log.",
    type=str,
    default=r"^.*$",
)
@click.option(
    "-r",
    "--repl",
    metavar="REPL",
    help="Replacement of match.",
    type=str,
)
@click.option(
    "-u",
    "--unique",
    is_flag=True,
    default=False,
    help="Return only unique match.",
)
@click.option(
    "-s",
    "--sort",
    is_flag=True,
    default=False,
    help="Sort match in alphabetical order.",
)
def minelog_cli(
    directory: Optional[pathlib.Path],
    pattern: str,
    repl: Optional[str],
    *,
    unique: bool,
    sort: bool,
) -> None:
    """Run hello command."""
    minelog = MineLog(directory)
    for result in minelog.search_bytes(
        pattern.encode(MC_ENCODING),
        repl=None if repl is None else repl.encode(MC_ENCODING),
        unique=unique,
        sort=sort,
    ):
        click.echo(result.decode(MC_ENCODING))
