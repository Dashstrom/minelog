"""Core module, contains all core functions."""


import gzip
import pathlib
import platform
import re
from typing import IO, Iterator, Optional, Tuple, Union, cast

RE_FILE_ARCHIVE_GROUP = re.compile(
    r"^(20[0-9]{2}-[01][0-9]-[0-3][0-9])-([0-9]{1,2}).log.gz$",
)
BUFFER_SIZE = 1024 * 1024
RegexType = Union[str, bytes, "re.Pattern[bytes]", "re.Pattern[str]"]


def minecraft_path() -> pathlib.Path:
    """Return the path to minecraft folder."""
    home = pathlib.Path.home()
    if platform.system() == "Darwin":
        return home / "Library" / "Application Support " / "minecraft"
    if platform.system() == "Windows":
        return home / "AppData" / "Roaming" / ".minecraft"
    return home / ".minecraft"


class LogMatch:
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

    def __init__(self, path: Optional[pathlib.Path] = None) -> None:
        """Create a MineLog instance."""
        if path is None:
            self.folder = minecraft_path() / "logs"
        else:
            self.folder = path

    def iteropen(self) -> Iterator[Tuple[pathlib.Path, IO[bytes]]]:
        """Iterate over all file and open them."""
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

    def compile(self, pattern: RegexType) -> "re.Pattern[bytes]":
        """Compile the regex."""
        if isinstance(pattern, re.Pattern):
            if isinstance(pattern.pattern, str):
                return re.compile(
                    pattern.pattern.encode("ansi"),
                    pattern.flags,
                )
            return pattern
        if isinstance(pattern, str):
            pattern = pattern.encode("ansi")
        return re.compile(pattern, re.MULTILINE)

    def search(self, pattern: RegexType) -> Iterator[LogMatch]:
        """Search among all logs."""
        regex = self.compile(pattern)
        for path, file in self.iteropen():
            for match in regex.finditer(file.read()):
                yield LogMatch(match, path)

    def __repr__(self) -> str:
        """Reprensent."""
        return f"MineLog({self.folder!r})"
