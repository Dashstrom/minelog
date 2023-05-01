"""Main package."""
from .cli import minelog_cli
from .core import MineLog
from .info import (
    __author__,
    __copyright__,
    __description__,
    __email__,
    __license__,
    __maintainer__,
    __version__,
)

__all__ = [
    "minelog_cli",
    "MineLog",
    "__author__",
    "__copyright__",
    "__description__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__version__",
]
