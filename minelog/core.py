"""Core module, contains all core functions."""


import gzip
import pathlib
import platform
import re
from typing import IO, Callable, Iterator, Optional, Set, Tuple, Union, cast

RE_FILE_ARCHIVE_GROUP = re.compile(
    r"^(20[0-9]{2}-[01][0-9]-[0-3][0-9])-([0-9]{1,2}).log.gz$",
)
MC_ENCODING = "ansi"
RegexType = Union[bytes, "re.Pattern[bytes]"]
ReplType = Union[bytes, Callable[["re.Match[bytes]"], bytes]]


def minecraft_path() -> pathlib.Path:
    """Return the path to minecraft folder."""
    home = pathlib.Path.home()
    if platform.system() == "Darwin":
        return home / "Library" / "Application Support " / "minecraft"
    if platform.system() == "Windows":
        return home / "AppData" / "Roaming" / ".minecraft"
    return home / ".minecraft"


class LogEntry:
    """Class for representing a match inside a file."""

    __slots__ = "match", "path"

    def __init__(self, match: "re.Match[bytes]", path: pathlib.Path) -> None:
        """Create a LogMatch instance."""
        self.match = match
        self.path = path

    def __repr__(self) -> str:
        return f"LogMatch({self.path!r}, {self.match!r})"


class MineLog:
    """Class for search in minecraft logs."""

    def __init__(self, path: Optional[pathlib.Path] = None, /) -> None:
        """Create a MineLog instance."""
        if path is None:
            self.folder = minecraft_path() / "logs"
        else:
            self.folder = path

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

    def iteropen(self) -> Iterator[Tuple[pathlib.Path, IO[bytes]]]:
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

    def itermatch(self, pattern: RegexType, /) -> Iterator[LogEntry]:
        """Iterate over all match found inside logs."""
        regex = self.compile(pattern)
        for path, file in self.iteropen():
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
        previous: Set[bytes] = set()
        regex = self.compile(pattern)
        for match in self.itermatch(regex):
            record = match.match.group(0)
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
        """Reprensent MineLog."""
        return f"MineLog({self.folder!r})"
