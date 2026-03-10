from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_float


def normalize_sentiments_ticker(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "data": [
        {"date": "2026-01-19", "score": 0.265},
        {"date": "2026-01-16", "score": 0.346},
        ...
      ]
    }
    -> {"ticker","name","series":[{"date","score"},...]}  (dates sorted)
    """
    obj = obj or {}
    arr = obj.get("data") or []
    series: List[Dict] = [
        {"date": it.get("date"), "score": to_float(it.get("score"))}
        for it in arr
        if isinstance(it, dict)
    ]
    series.sort(key=lambda r: r["date"])
    return {
        "ticker": obj.get("symbol"),
        "name": obj.get("name"),
        "series": series,
    }
