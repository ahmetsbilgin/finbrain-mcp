from __future__ import annotations
from typing import Any, List, Dict
from .shared import to_float, pct_to_text


def normalize_screener_predictions(items: Any) -> List[Dict]:
    """
    V2 screener predictions (after SDK unwrap).
    Items is a list of per-ticker prediction summaries returned by
    /screener/predictions/daily or /screener/predictions/monthly.

    Each item shape:
    {
      "symbol": "STX",
      "name": "Seagate Technology",
      "expectedShortTerm": 1.24,
      "expectedMidTerm": 2.56,
      "expectedLongTerm": 3.12,
      "lastUpdated": "2026-01-19T..."
    }

    -> flat rows with percent-formatted expected returns.
    """
    out: list[dict] = []
    if not isinstance(items, list):
        return out
    for it in items:
        if not isinstance(it, dict):
            continue
        short_pct = to_float(it.get("expectedShortTerm"))
        mid_pct = to_float(it.get("expectedMidTerm"))
        long_pct = to_float(it.get("expectedLongTerm"))
        out.append(
            {
                "ticker": it.get("symbol"),
                "name": it.get("name"),
                "expected_short": pct_to_text(short_pct),
                "expected_mid": pct_to_text(mid_pct),
                "expected_long": pct_to_text(long_pct),
                "last_update": it.get("lastUpdated"),
            }
        )
    return out


def normalize_ticker_predictions(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "type": "daily",
      "predictions": [
        {"date": "2026-01-16", "mid": 255.21, "lower": 251.01, "upper": 259.48},
        ...
      ],
      "metadata": {
        "expectedShortTerm": 0.17,
        "expectedMidTerm": 0.47,
        "expectedLongTerm": 1.22,
        "lowerBoundChange": -3.95,
        "upperBoundChange": 6.67
      },
      "lastUpdated": "2026-01-19T15:05:59.853Z"
    }

    -> normalized object with `series` array and parsed metadata.
    """
    obj = obj or {}
    meta = obj.get("metadata") or {}
    short_pct = to_float(meta.get("expectedShortTerm"))
    mid_pct = to_float(meta.get("expectedMidTerm"))
    long_pct = to_float(meta.get("expectedLongTerm"))

    preds = obj.get("predictions") or []
    series: list[dict] = []
    for p in preds:
        if not isinstance(p, dict):
            continue
        series.append(
            {
                "date": p.get("date"),
                "mid": to_float(p.get("mid")),
                "low": to_float(p.get("lower")),
                "high": to_float(p.get("upper")),
            }
        )
    series.sort(key=lambda r: r["date"])

    return {
        "ticker": obj.get("symbol"),
        "name": obj.get("name"),
        "type": obj.get("type"),
        "last_update": obj.get("lastUpdated"),
        "expected_short": pct_to_text(short_pct),
        "expected_mid": pct_to_text(mid_pct),
        "expected_long": pct_to_text(long_pct),
        "series": series,
    }
