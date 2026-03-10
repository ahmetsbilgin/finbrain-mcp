from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_float, to_int


def normalize_app_ratings_ticker(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "AMZN",
      "name": "Amazon.com Inc",
      "data": [
        {
          "date": "2024-02-02",
          "ios": {"score": 4.07, "ratingsCount": 88533},
          "android": {"score": 3.75, "ratingsCount": 567996, "installCount": null}
        },
        ...
      ]
    }

    -> {
      "ticker": "AMZN",
      "name": "Amazon.com Inc",
      "series": [
        {
          "date": "2024-02-02",
          "play_store_score": 3.75,
          "play_store_ratings_count": 567996,
          "app_store_score": 4.07,
          "app_store_ratings_count": 88533,
          "play_store_install_count": None
        },
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
        ios = it.get("ios") or {}
        android = it.get("android") or {}
        series.append(
            {
                "date": it.get("date"),
                "play_store_score": to_float(android.get("score")),
                "play_store_ratings_count": to_int(android.get("ratingsCount")),
                "app_store_score": to_float(ios.get("score")),
                "app_store_ratings_count": to_int(ios.get("ratingsCount")),
                "play_store_install_count": to_int(android.get("installCount")),
            }
        )
    series.sort(key=lambda r: r["date"])
    return {
        "ticker": obj.get("symbol"),
        "name": obj.get("name"),
        "series": series,
    }
