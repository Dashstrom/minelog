"""Module for use module as a cli."""
import pathlib
from typing import Optional

import click

from .core import MineLog
from .info import __copyright__, __description__, __version__


@click.command("minelog", help=__description__, epilog=__copyright__)
@click.version_option(__version__)
@click.option(
    "-d",
    "--directory",
    help="path to search",
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
    help="path to search",
    type=str,
    default=r"^(.*)$",
)
@click.option("-r", "--repl", help="path to search", type=str, default=r"\1")
@click.option(
    "-u",
    "--unique",
    is_flag=True,
    default=False,
    help="path to search",
)
@click.option(
    "-s",
    "--sort",
    is_flag=True,
    default=False,
    help="path to search",
)
def minelog_cli(
    directory: Optional[pathlib.Path],
    pattern: str,
    repl: str,
    *,
    unique: bool = False,
    sort: bool = False,
) -> None:
    """Run hello command."""
    previous = set()
    minelog = MineLog(directory)
    regex = minelog.compile(pattern)
    for match in minelog.search(regex):
        text = match.match.group(0)
        record = regex.sub(repl.encode("ansi"), text, 1)
        if unique and record in previous:
            continue
        if unique or sort:
            previous.add(record)
        if not sort:
            click.echo(record.decode("ansi"))
    if sort:
        for record in sorted(previous):
            click.echo(record)
