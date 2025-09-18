from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_float, to_int


def normalize_app_ratings_ticker(obj: Any) -> Dict:
    """
    RAW:
    {
      "ticker": "AMZN",
      "name": "Amazon.com Inc",
      "appRatings": [
        {
          "playStoreScore": 3.75,
          "playStoreRatingsCount": 567996,
          "appStoreScore": 4.07,
          "appStoreRatingsCount": 88533,
          "playStoreInstallCount": null,
          "date": "2024-02-02"
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
    arr = obj.get("appRatings") or []
    series: List[Dict] = []
    for it in arr:
        if not isinstance(it, dict):
            continue
        series.append(
            {
                "date": it.get("date"),
                "play_store_score": to_float(it.get("playStoreScore")),
                "play_store_ratings_count": to_int(it.get("playStoreRatingsCount")),
                "app_store_score": to_float(it.get("appStoreScore")),
                "app_store_ratings_count": to_int(it.get("appStoreRatingsCount")),
                "play_store_install_count": to_int(it.get("playStoreInstallCount")),
            }
        )
    series.sort(key=lambda r: r["date"])
    return {
        "ticker": obj.get("ticker"),
        "name": obj.get("name"),
        "series": series,
    }
