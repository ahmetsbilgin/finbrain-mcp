from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_int


def normalize_linkedin_ticker(obj: Any) -> Dict:
    """
    RAW:
    {
      "ticker": "AMZN",
      "name": "Amazon.com Inc.",
      "linkedinData": [
        {"date": "2024-03-20", "employeeCount": 755461, "followersCount": 30628460},
        ...
      ]
    }

    -> {
      "ticker": "AMZN",
      "name": "Amazon.com Inc.",
      "series": [
        {"date": "2024-03-20", "employee_count": 755461, "followers_count": 30628460},
        ...
      ]
    }
    """
    obj = obj or {}
    arr = obj.get("linkedinData") or []
    series: List[Dict] = []
    for it in arr:
        if not isinstance(it, dict):
            continue
        series.append(
            {
                "date": it.get("date"),
                "employee_count": to_int(it.get("employeeCount")),
                "followers_count": to_int(it.get("followersCount")),
            }
        )
    series.sort(key=lambda r: r["date"])
    return {
        "ticker": obj.get("ticker"),
        "name": obj.get("name"),
        "series": series,
    }
