from __future__ import annotations
from typing import Any, Dict, List
import re
from .shared import to_float

_price_re = re.compile(r"[-+]?\d+(?:\.\d+)?")


def _parse_price_pair(s: Any) -> tuple[float | None, float | None]:
    """
    Parses strings like "$205 → $190", "$189 -> $200" or "205 to 190" into (205.0, 190.0).
    Returns (None, None) if not found.
    """
    if s is None:
        return (None, None)
    text = str(s).replace(",", "")
    nums = _price_re.findall(text)
    if not nums:
        return (None, None)
    if len(nums) == 1:
        return (to_float(nums[0]), None)
    return (to_float(nums[0]), to_float(nums[1]))


def normalize_analyst_ratings_ticker(obj: Any) -> Dict:
    """
    RAW:
    {
      "ticker": "AMZN",
      "name": "Amazon.com Inc.",
      "analystRatings": [
        {"date":"2024-02-02","type":"Reiterated","institution":"Piper Sandler","signal":"Neutral","targetPrice":"$205 → $190"},
        ...
      ]
    }

    -> {
      "ticker": "...",
      "name": "...",
      "series": [
        {
          "date": "2024-02-02",
          "rating_type": "Reiterated",
          "institution": "Piper Sandler",
          "signal": "Neutral",
          "target_price_from": 205.0,
          "target_price_to": 190.0,
          "target_price_raw": "$205 → $190"
        }, ...
      ]
    }
    """
    obj = obj or {}
    arr = obj.get("analystRatings") or []
    series: List[Dict] = []
    for it in arr:
        if not isinstance(it, dict):
            continue
        p_from, p_to = _parse_price_pair(it.get("targetPrice"))
        series.append(
            {
                "date": it.get("date"),
                "rating_type": it.get("type"),
                "institution": it.get("institution"),
                "signal": it.get("signal"),
                "target_price_from": p_from,
                "target_price_to": p_to,
                "target_price_raw": it.get("targetPrice"),
            }
        )
    series.sort(key=lambda r: r["date"])
    return {
        "ticker": obj.get("ticker"),
        "name": obj.get("name"),
        "series": series,
    }
