from __future__ import annotations
from typing import Any, List


def normalize_available_markets(obj: Any) -> List[str]:
    """
    V2 RAW (after SDK envelope unwrap):
    The SDK returns a list of market objects:
      [{"name": "S&P 500", ...}, {"name": "NASDAQ", ...}, ...]
    or in some cases already a list of strings.

    -> ["S&P 500", "NASDAQ", ...]
    """
    if not isinstance(obj, list):
        return []
    if not obj:
        return []
    # v2: list of dicts with "name" key
    if isinstance(obj[0], dict):
        return [it.get("name", "") for it in obj if isinstance(it, dict)]
    # fallback: already a list of strings
    return obj
