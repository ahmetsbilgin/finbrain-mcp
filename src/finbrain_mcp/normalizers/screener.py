from __future__ import annotations
from typing import Any, List, Dict
from .shared import to_float, to_int


def _rows(data: Any) -> list:
    """Ensure data is a list."""
    if isinstance(data, list):
        return data
    return []


def normalize_screener_sentiment(items: Any) -> List[Dict]:
    """
    V2 screener sentiment rows.
    [{symbol, name, date, score}] -> [{ticker, name, date, score}]
    """
    out: list[dict] = []
    for it in _rows(items):
        if not isinstance(it, dict):
            continue
        out.append(
            {
                "ticker": it.get("symbol"),
                "name": it.get("name"),
                "date": it.get("date"),
                "score": to_float(it.get("score")),
            }
        )
    return out


def normalize_screener_analyst_ratings(items: Any) -> List[Dict]:
    """
    V2 screener analyst ratings rows.
    [{symbol, name, date, institution, action, rating, targetPrice}]
    -> [{ticker, name, date, institution, rating_type, signal, target_price}]
    """
    out: list[dict] = []
    for it in _rows(items):
        if not isinstance(it, dict):
            continue
        out.append(
            {
                "ticker": it.get("symbol"),
                "name": it.get("name"),
                "date": it.get("date"),
                "institution": it.get("institution"),
                "rating_type": it.get("action"),
                "signal": it.get("rating"),
                "target_price": it.get("targetPrice"),
            }
        )
    return out


def normalize_screener_insider_trading(items: Any) -> List[Dict]:
    """
    V2 screener insider trading rows.
    [{symbol, name, date, insider, relationship, transactionType, shares, totalValue}]
    -> [{ticker, name, date, insider_name, relationship, transaction_type, shares, total_value}]
    """
    out: list[dict] = []
    for it in _rows(items):
        if not isinstance(it, dict):
            continue
        out.append(
            {
                "ticker": it.get("symbol"),
                "name": it.get("name"),
                "date": it.get("date"),
                "insider_name": it.get("insider"),
                "relationship": it.get("relationship"),
                "transaction_type": it.get("transactionType"),
                "shares": to_int(it.get("shares")),
                "total_value": to_float(it.get("totalValue")),
            }
        )
    return out


def normalize_screener_congress(items: Any) -> List[Dict]:
    """
    V2 screener congress (house/senate) rows.
    [{symbol, name, date, politician, transactionType, amount}]
    -> [{ticker, name, date, politician, trade_type, amount}]
    """
    out: list[dict] = []
    for it in _rows(items):
        if not isinstance(it, dict):
            continue
        out.append(
            {
                "ticker": it.get("symbol"),
                "name": it.get("name"),
                "date": it.get("date"),
                "politician": it.get("politician"),
                "trade_type": it.get("transactionType"),
                "amount": it.get("amount"),
            }
        )
    return out


def normalize_screener_news(items: Any) -> List[Dict]:
    """
    V2 screener news rows.
    [{symbol, name, date, headline, source, url}]
    -> [{ticker, name, date, headline, source, url}]
    """
    out: list[dict] = []
    for it in _rows(items):
        if not isinstance(it, dict):
            continue
        out.append(
            {
                "ticker": it.get("symbol"),
                "name": it.get("name"),
                "date": it.get("date"),
                "headline": it.get("headline"),
                "source": it.get("source"),
                "url": it.get("url"),
            }
        )
    return out


def normalize_screener_put_call(items: Any) -> List[Dict]:
    """
    V2 screener put/call ratio rows.
    [{symbol, name, date, ratio, callVolume, putVolume}]
    -> [{ticker, name, date, put_call_ratio, call_count, put_count}]
    """
    out: list[dict] = []
    for it in _rows(items):
        if not isinstance(it, dict):
            continue
        out.append(
            {
                "ticker": it.get("symbol"),
                "name": it.get("name"),
                "date": it.get("date"),
                "put_call_ratio": to_float(it.get("ratio")),
                "call_count": to_int(it.get("callVolume")),
                "put_count": to_int(it.get("putVolume")),
            }
        )
    return out


def normalize_screener_linkedin(items: Any) -> List[Dict]:
    """
    V2 screener LinkedIn data rows.
    [{symbol, name, date, employeeCount, followerCount, jobCount}]
    -> [{ticker, name, date, employee_count, followers_count, job_count}]
    """
    out: list[dict] = []
    for it in _rows(items):
        if not isinstance(it, dict):
            continue
        out.append(
            {
                "ticker": it.get("symbol"),
                "name": it.get("name"),
                "date": it.get("date"),
                "employee_count": to_int(it.get("employeeCount")),
                "followers_count": to_int(it.get("followerCount")),
                "job_count": to_int(it.get("jobCount")),
            }
        )
    return out


def normalize_screener_app_ratings(items: Any) -> List[Dict]:
    """
    V2 screener app ratings rows.
    [{symbol, name, date, iosRating, androidRating}]
    -> [{ticker, name, date, app_store_score, play_store_score}]
    """
    out: list[dict] = []
    for it in _rows(items):
        if not isinstance(it, dict):
            continue
        out.append(
            {
                "ticker": it.get("symbol"),
                "name": it.get("name"),
                "date": it.get("date"),
                "app_store_score": to_float(it.get("iosRating")),
                "play_store_score": to_float(it.get("androidRating")),
            }
        )
    return out
