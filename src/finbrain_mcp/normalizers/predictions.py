from __future__ import annotations
from typing import Any, List, Dict
from .shared import to_float, parse_mid_low_high, pct_to_text


def normalize_market_predictions(items: Any) -> List[Dict]:
    """
    RAW list:
      {
        "ticker": "STX",
        "name": "Seagate Technology",
        "prediction": {
          "expectedShort": "1.24632", "expectedMid": "...", "expectedLong": "...",
          "technicalAnalysis": "...", "lastUpdate": "...", "type": "daily"
        },
        "sentimentScore": "-0.137"
      }
    -> flat rows with numeric fields parsed
    """
    out: list[dict] = []
    if not isinstance(items, list):
        return out
    for it in items:
        pred = (it or {}).get("prediction", {}) if isinstance(it, dict) else {}
        short_pct = to_float(pred.get("expectedShort"))
        mid_pct = to_float(pred.get("expectedMid"))
        long_pct = to_float(pred.get("expectedLong"))
        out.append(
            {
                "ticker": it.get("ticker"),
                "name": it.get("name"),
                # single, unambiguous representation (percent string)
                "expected_short": pct_to_text(short_pct),
                "expected_mid": pct_to_text(mid_pct),
                "expected_long": pct_to_text(long_pct),
                "technical_analysis": pred.get("technicalAnalysis"),
                "last_update": pred.get("lastUpdate"),
                "type": pred.get("type"),
                "sentiment_score": to_float(it.get("sentimentScore")),
            }
        )
    return out


def normalize_ticker_predictions(obj: Any) -> Dict:
    """
    RAW object:
      {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "prediction": {
          "YYYY-MM-DD": "mid,low,high",
          "expectedShort": "0.22", "expectedMid": "0.58", "expectedLong": "0.25",
          "technicalAnalysis": "...", "type": "daily", "lastUpdate": "..."
        },
        "sentimentAnalysis": { "YYYY-MM-DD": "0.186", ... }
      }
    -> normalized object with `series` and `sentiment` arrays, floats parsed.
    """
    obj = obj or {}
    pred = obj.get("prediction", {}) if isinstance(obj, dict) else {}
    # extract meta
    short_pct = to_float(pred.get("expectedShort"))
    mid_pct = to_float(pred.get("expectedMid"))
    long_pct = to_float(pred.get("expectedLong"))
    series: list[dict] = []
    for k, v in pred.items():
        if k in {
            "expectedShort",
            "expectedMid",
            "expectedLong",
            "technicalAnalysis",
            "type",
            "lastUpdate",
        }:
            continue
        series.append({"date": k, **parse_mid_low_high(v)})
    series.sort(key=lambda r: r["date"])

    sent = obj.get("sentimentAnalysis") or {}
    sentiment = [{"date": d, "score": to_float(s)} for d, s in sent.items()]
    sentiment.sort(key=lambda r: r["date"])

    return {
        "ticker": obj.get("ticker"),
        "name": obj.get("name"),
        "type": pred.get("type"),
        "last_update": pred.get("lastUpdate"),
        # single, unambiguous representation (percent string)
        "expected_short": pct_to_text(short_pct),
        "expected_mid": pct_to_text(mid_pct),
        "expected_long": pct_to_text(long_pct),
        "technical_analysis": pred.get("technicalAnalysis"),
        "series": series,
        "sentiment": sentiment,
    }
