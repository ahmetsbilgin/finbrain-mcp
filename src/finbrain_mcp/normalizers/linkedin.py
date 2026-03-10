from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_int


def normalize_linkedin_ticker(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "AMZN",
      "name": "Amazon.com Inc.",
      "data": [
        {"date": "2026-01-14", "employeeCount": 166090,
         "followerCount": 18039757, "jobCount": null},
        ...
      ]
    }

    -> {
      "ticker": "AMZN",
      "name": "Amazon.com Inc.",
      "series": [
        {"date": "2026-01-14", "employee_count": 166090, "followers_count": 18039757},
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
                "employee_count": to_int(it.get("employeeCount")),
                "followers_count": to_int(it.get("followerCount")),
            }
        )
    series.sort(key=lambda r: r["date"])
    return {
        "ticker": obj.get("symbol"),
        "name": obj.get("name"),
        "series": series,
    }
