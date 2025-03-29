"""Core module, contains all core functions."""

import gzip
import pathlib
import platform
import re
from collections.abc import Iterator
from typing import IO, Callable, Optional, Union, cast

RE_FILE_ARCHIVE_GROUP = re.compile(
    r"^(?P<date>20[0-9]{2}-[01][0-9]-[0-3][0-9])-(?P<number>[0-9]{1,2}).log.gz$",
)
MC_ENCODING = "utf-8"
RegexType = Union[bytes, "re.Pattern[bytes]"]
ReplType = Union[bytes, Callable[["re.Match[bytes]"], bytes]]


def minecraft_path() -> pathlib.Path:
    """Return the path to minecraft folder."""
    home = pathlib.Path.home().resolve()
    if platform.system() == "Darwin":
        return home / "Library" / "Application Support " / "minecraft"
    if platform.system() == "Windows":
        return home / "AppData" / "Roaming" / ".minecraft"
    return pathlib.Path.cwd().resolve()


class LogEntry:
    """Class for representing a match inside a file."""

    __slots__ = "match", "path"

    def __init__(self, match: "re.Match[bytes]", path: pathlib.Path) -> None:
        """Create a LogMatch instance."""
        self.match = match
        self.path = path

    @property
    def content(self) -> bytes:
        """Return the log content."""
        return self.match[0]

    @property
    def date(self) -> bytes:
        """Return the date of the log."""
        return self.match["date"]

    @property
    def number(self) -> int:
        """Return number of the log."""
        return int(self.match["number"].decode("utf-8"))

    def __repr__(self) -> str:
        """Represent the log match."""
        return f"LogMatch({self.path!r}, {self.match!r})"


class MineLog:
    """Class for search in minecraft logs."""

    def __init__(self, path: Optional[pathlib.Path] = None, /) -> None:
        """Create a MineLog instance."""
        if path is None:
            self.folder = minecraft_path() / "logs"
        else:
            self.folder = path
        if not self.folder.is_dir():
            error_message = (
                f"{self.folder!r} is not a directory, "
                "please specify a valid one."
            )
            raise NotADirectoryError(error_message)

    def compile(self, pattern: RegexType, /) -> "re.Pattern[bytes]":
        """Compile the regex."""
        if isinstance(pattern, re.Pattern):
            if isinstance(pattern.pattern, str):
                msg = (
                    "pattern should be bytes or re.Pattern[bytes] "
                    "not re.Pattern[str]"
                )
                raise TypeError(msg)
            return pattern
        if isinstance(pattern, str):
            msg = (
                "pattern should be bytes or re.Pattern[bytes] "
                f"not {type(pattern)}"
            )
            raise TypeError(msg)
        return re.compile(pattern, re.MULTILINE)

    def iter_open(self) -> Iterator[tuple[pathlib.Path, IO[bytes]]]:
        """Iterate over all files and open them."""
        for archive_path in sorted(self.folder.iterdir()):
            match = RE_FILE_ARCHIVE_GROUP.fullmatch(archive_path.name)
            if match:
                with gzip.GzipFile(archive_path, "r") as gzipfile:
                    yield archive_path, cast(IO[bytes], gzipfile)
        latest = self.folder / "latest.log"
        try:
            with latest.open("rb") as file:
                yield latest, file
        except FileNotFoundError:
            pass

    def iter_match(self, pattern: RegexType, /) -> Iterator[LogEntry]:
        """Iterate over all match found inside logs."""
        regex = self.compile(pattern)
        for path, file in self.iter_open():
            for match in regex.finditer(file.read()):
                yield LogEntry(match, path)

    def search_bytes(
        self,
        pattern: RegexType,
        /,
        *,
        repl: Optional[ReplType] = None,
        unique: Optional[bool] = False,
        sort: Optional[bool] = False,
    ) -> Iterator[bytes]:
        """Search and return replacement with a regex."""
        previous: set[bytes] = set()
        regex = self.compile(pattern)
        for match in self.iter_match(regex):
            record = match.content
            if repl is not None:
                record = regex.sub(repl, record, 1)
            if unique and record in previous:
                continue
            if unique or sort:
                previous.add(record)
            if not sort:
                yield record
        if sort:
            for record in sorted(previous):
                yield record

    def __repr__(self) -> str:
        """Represent a MineLog."""
        return f"MineLog({self.folder!r})"
