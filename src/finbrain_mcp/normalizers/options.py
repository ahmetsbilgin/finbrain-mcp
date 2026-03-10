from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_int, to_float


def normalize_options_put_call_ticker(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "AMZN",
      "name": "Amazon.com Inc.",
      "data": [
        {"date": "2026-01-19", "ratio": 0.5, "callVolume": 620689,
         "putVolume": 310344, "totalVolume": 931034, "price": 255.53},
        ...
      ]
    }

    -> {
      "ticker": "AMZN",
      "name": "Amazon.com Inc.",
      "series": [
        {"date": "2026-01-19", "put_call_ratio": 0.5,
         "call_count": 620689, "put_count": 310344},
        ...
      ]
    }
    """
    obj = obj or {}
    arr = obj.get("data") or []
    series: List[Dict] = []
    for it in arr:
        if not isinstance(it, dict):
            continue
        series.append(
            {
                "date": it.get("date"),
                "put_call_ratio": to_float(it.get("ratio")),
                "call_count": to_int(it.get("callVolume")),
                "put_count": to_int(it.get("putVolume")),
            }
        )
    series.sort(key=lambda r: r["date"])
    return {
        "ticker": obj.get("symbol"),
        "name": obj.get("name"),
        "series": series,
    }
