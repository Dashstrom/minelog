"""Module holding metadata."""

from importlib.metadata import Distribution

_DISTRIBUTION = Distribution.from_name(
    "minelog",
)
_METADATA = _DISTRIBUTION.metadata

if "Author" in _METADATA:
    __author__ = str(_METADATA["Author"])
    __email__ = str(_METADATA["Author-email"])
else:
    __author__, __email__ = _METADATA["Author-email"][:-1].split(" <", 1)
__version__ = _METADATA["Version"]
__summary__ = _METADATA["Summary"]
__copyright__ = f"{__author__} <{__email__}>"
__issues__ = "https://github.com/Dashstrom/minelog/issues"
