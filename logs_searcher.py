
import os
import re
import gzip
import sys
import platform

from typing import Generator


PATH = os.path.dirname(os.path.abspath(__file__))
_platform = platform.system()
if _platform == "Darwin":
    DEFAULT_PATH = "~/Library/Application Support/minecraft"
elif _platform == "Windows":
    DEFAULT_PATH = os.path.join(os.path.expandvars("%userprofile%"),
                                "AppData//Roaming//.minecraft//logs")
else:
    DEFAULT_PATH = "~/.minecraft"

DEFAULT_PATH = os.path.abspath(DEFAULT_PATH)
RE_FILE_ARCHIVE_GROUP = re.compile(
    r"^(20[0-9]{2}-[01][0-9]-[0-3][0-9])-([0-9]{1,2}).log.gz")
BUFFER_SIZE = 1024 * 1024


def match_lines(
    text: str, patern: re.Pattern, prefix: str
) -> Generator[str, None, None]:
    """Yield matched lines with format."""
    for n, line in enumerate(text.strip().split("\n")):
        if patern.search(line):
            yield f"[{prefix}][{n:6}] {line}"


def search(
    regex: str, path_archives: str = DEFAULT_PATH
) -> Generator[str, None, None]:
    """Search into minecraft logs."""
    patern = re.compile(regex)
    for archive in os.listdir(path_archives):
        if match := RE_FILE_ARCHIVE_GROUP.fullmatch(archive):
            path = os.path.join(path_archives, archive)
            raw_log = bytes()
            with gzip.GzipFile(path, "r") as gzipfile:
                data = gzipfile.read(BUFFER_SIZE)
                while data:
                    raw_log += data
                    data = gzipfile.read(BUFFER_SIZE)
            text_log = raw_log.decode("ansi")
            yield from match_lines(text_log, patern, match[1])
    latest = os.path.join(path_archives, "latest.log")
    try:
        with open(latest, "r", encoding="ansi") as file:
            text = file.read()
        yield from match_lines(text, patern, "latest.log")
    except OSError:
        pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scearch into Minecraft logs")
    parser.add_argument("matcher", help="text or regex to match")
    parser.add_argument("-p", "--path", help="path to search")
    parser.add_argument("-r", "--regex", help="allow to use regex",
                        action="store_true")
    args = parser.parse_args()
    regex = args.matcher if args.regex else re.escape(args.matcher)
    if args.path:
        searcher = search(regex, args.path)
    else:
        if not os.path.isdir(DEFAULT_PATH):
            print("Default path is wrong please specify path with argument -p")
            sys.exit(1)
        searcher = search(regex)

    for line in searcher:
        print(line)
