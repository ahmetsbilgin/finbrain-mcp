from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_int, to_float


def normalize_reddit_mentions_ticker(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "TSLA",
      "name": "Tesla, Inc.",
      "data": [
        {"date": "2026-03-17T08:00:00.000Z", "subreddit": "_all", "mentions": 120},
        {"date": "2026-03-17T08:00:00.000Z", "subreddit": "wallstreetbets", "mentions": 85},
        ...
      ]
    }

    -> {
      "ticker": "TSLA",
      "name": "Tesla, Inc.",
      "series": [
        {"date": "2026-03-17T08:00:00.000Z", "subreddit": "_all", "mentions": 120},
        ...
      ]
    }
    """
    obj = obj or {}
    rows = obj.get("data") or []
    series: List[Dict] = []
    for it in rows:
        if not isinstance(it, dict):
            continue
        series.append(
            {
                "date": it.get("date"),
                "subreddit": it.get("subreddit"),
                "mentions": to_int(it.get("mentions")),
            }
        )
    series.sort(key=lambda r: r["date"] or "")
    return {"ticker": obj.get("symbol"), "name": obj.get("name"), "series": series}


def normalize_screener_reddit_mentions(items: Any) -> List[Dict]:
    """
    V2 screener reddit mentions rows.
    [{symbol, name, date, totalMentions, subreddits: {name: count}}]
    -> [{ticker, name, date, total_mentions, subreddits: {name: count}}]
    """
    out: list[dict] = []
    if not isinstance(items, list):
        return out
    for it in items:
        if not isinstance(it, dict):
            continue
        out.append(
            {
                "ticker": it.get("symbol"),
                "name": it.get("name"),
                "date": it.get("date"),
                "total_mentions": to_int(it.get("totalMentions")),
                "subreddits": it.get("subreddits") or {},
            }
        )
    return out


def normalize_screener_reddit_mentions_summary(summary: Any) -> Dict:
    """
    {totalEntries, totalTickers, averageMentions, topMentioned, subredditNames}
    -> {total_entries, total_tickers, average_mentions, top_mentioned, subreddit_names}
    """
    summary = summary or {}
    return {
        "total_entries": to_int(summary.get("totalEntries")),
        "total_tickers": to_int(summary.get("totalTickers")),
        "average_mentions": to_float(summary.get("averageMentions")),
        "top_mentioned": summary.get("topMentioned") or [],
        "subreddit_names": summary.get("subredditNames") or [],
    }
