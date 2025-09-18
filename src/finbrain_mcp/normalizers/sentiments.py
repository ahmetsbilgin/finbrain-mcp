from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_float


def normalize_sentiments_ticker(obj: Any) -> Dict:
    """
    RAW:
    {
      "ticker": "AMZN",
      "name": "Amazon.com Inc.",
      "sentimentAnalysis": {
          "2021-12-15": "0.223",
          "2021-12-14": "0.037",
          "2021-12-13": "-0.038"
      }
    }
    -> {"ticker","name","series":[{"date","score"},...]}  (dates sorted)
    """
    obj = obj or {}
    sa = obj.get("sentimentAnalysis") or {}
    series: List[Dict] = [{"date": d, "score": to_float(v)} for d, v in sa.items()]
    series.sort(key=lambda r: r["date"])  # ascending date order
    return {
        "ticker": obj.get("ticker"),
        "name": obj.get("name"),
        "series": series,
    }
