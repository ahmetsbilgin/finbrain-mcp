from __future__ import annotations
from typing import Any, Dict, List


def normalize_news_ticker(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "articles": [
        {
          "date": "2026-01-19",
          "headline": "Article headline",
          "source": "News source",
          "url": "https://...",
        },
        ...
      ]
    }

    -> {ticker, name, series: [{date, headline, source, url}, ...]}
    """
    obj = obj or {}
    articles = obj.get("articles") or []
    series: List[Dict] = []
    for a in articles:
        if not isinstance(a, dict):
            continue
        series.append(
            {
                "date": a.get("date"),
                "headline": a.get("headline"),
                "source": a.get("source"),
                "url": a.get("url"),
            }
        )
    series.sort(key=lambda r: r.get("date") or "")
    return {
        "ticker": obj.get("symbol"),
        "name": obj.get("name"),
        "series": series,
    }
