"""Module for command line interface."""

import logging
import pathlib
import sys
from functools import wraps
from typing import Callable, Optional, TypeVar

import click
from typing_extensions import ParamSpec

from .core import MC_ENCODING, MineLog
from .info import __issues__, __summary__, __version__

logger = logging.getLogger(__name__)
LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
P = ParamSpec("P")
T = TypeVar("T")


def verbosity(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator for logging."""
    func = click.option(
        "-v",
        "--verbose",
        help="verbose mode, enable INFO and DEBUG messages.",
        is_flag=True,
    )(func)

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        verbose = kwargs.pop("verbose", False)
        logging.basicConfig(
            level=logging.DEBUG if verbose else logging.WARNING,
            format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        )
        try:
            return func(*args, **kwargs)
        except Exception as err:  # noqa: BLE001  # pragma: no cover
            logger.critical("Unexpected error", exc_info=err)
            logger.critical("Please, report this error to %s.", __issues__)
            sys.exit(1)

    return wrapper


@click.command(
    name="minelog",
    help=__summary__,
)
@click.version_option(__version__)
@click.option(
    "-d",
    "--directory",
    metavar="DIR",
    help="Path to logs.",
    type=click.Path(
        exists=True,
        dir_okay=True,
        readable=True,
        path_type=pathlib.Path,
    ),
)
@click.option("-e", "--encoding", help="Encoding used.", default=MC_ENCODING)
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
def minelog_cli(  # noqa: PLR0913
    directory: Optional[pathlib.Path],
    pattern: str,
    repl: Optional[str],
    encoding: str,
    *,
    unique: bool,
    sort: bool,
) -> None:
    """Run hello command."""
    minelog = MineLog(directory)
    for result in minelog.search_bytes(
        pattern.encode(encoding),
        repl=None if repl is None else repl.encode(encoding),
        unique=unique,
        sort=sort,
    ):
        click.echo(result.decode(encoding))
