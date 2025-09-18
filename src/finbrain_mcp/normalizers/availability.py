from __future__ import annotations
from typing import Any, List


def normalize_available_markets(obj: Any) -> List[str]:
    """
    RAW:
      {"availableMarkets": ["S&P 500", "NASDAQ", ...]}
    or in some cases already a list.
    """
    if isinstance(obj, dict) and isinstance(obj.get("availableMarkets"), list):
        return obj["availableMarkets"]
    return obj if isinstance(obj, list) else []
