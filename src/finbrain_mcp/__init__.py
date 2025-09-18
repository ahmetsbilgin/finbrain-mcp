"""FinBrain MCP."""

from __future__ import annotations
from importlib.metadata import PackageNotFoundError, version as _v

try:  # installed (wheel / sdist / editable)
    __version__ = _v("finbrain-mcp")  # PyPI distribution name
except PackageNotFoundError:  # fresh git clone, not installed
    __version__ = "0.0.0.dev0"

__all__ = ["__version__"]
