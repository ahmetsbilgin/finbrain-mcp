from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_int, to_float


def normalize_options_put_call_ticker(obj: Any) -> Dict:
    """
    RAW:
    {
      "ticker": "AMZN",
      "name": "Amazon.com Inc.",
      "putCallData": [
        {"date": "2024-03-19", "ratio": 0.4, "callCount": 788319, "putCount": 315327},
        ...
      ]
    }

    -> {
      "ticker": "AMZN",
      "name": "Amazon.com Inc.",
      "series": [
        {"date": "2024-03-19", "put_call_ratio": 0.4, "call_count": 788319, "put_count": 315327},
        ...
      ]
    }
    """
    obj = obj or {}
    arr = obj.get("putCallData") or []
    series: List[Dict] = []
    for it in arr:
        if not isinstance(it, dict):
            continue
        series.append(
            {
                "date": it.get("date"),
                "put_call_ratio": to_float(it.get("ratio")),
                "call_count": to_int(it.get("callCount")),
                "put_count": to_int(it.get("putCount")),
            }
        )
    series.sort(key=lambda r: r["date"])
    return {
        "ticker": obj.get("ticker"),
        "name": obj.get("name"),
        "series": series,
    }
