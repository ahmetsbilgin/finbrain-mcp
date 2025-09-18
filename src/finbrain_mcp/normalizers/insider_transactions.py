from __future__ import annotations
from typing import Any, Dict, List
from datetime import datetime
from .shared import to_float, to_int


def _parse_short_date(s: str | None) -> str | None:
    """
    'Mar 08 '24' -> '2024-03-08'
    """
    if not s:
        return None
    try:
        dt = datetime.strptime(s, "%b %d '%y")
        return dt.date().isoformat()
    except Exception:
        return None


def _parse_iso_date(s: str | None) -> str | None:
    if not s:
        return None
    try:
        # handle trailing Z
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        return datetime.fromisoformat(s).date().isoformat()
    except Exception:
        return None


def normalize_insider_transactions_ticker(obj: Any) -> Dict:
    """
    RAW:
    {
      "ticker": "AMZN",
      "name": "Amazon.com Inc.",
      "insiderTransactions": [
        {
          "date": "Mar 08 '24",
          "insiderTradings": "Selipsky Adam",
          "relationship": "CEO Amazon Web Services",
          "transaction": "Sale",
          "cost": 176.31,
          "shares": 500,
          "USDValue": 88155,
          "totalShares": 133100,
          "SECForm4Date": "2001-03-11T16:34:00.000Z",
          "SECForm4Link": "http://www.sec.gov/..."
        }, ...
      ]
    }

    -> {
      "ticker","name",
      "series":[
        {
          "date": "2024-03-08",          # ISO if parseable, otherwise original
          "date_raw": "Mar 08 '24",
          "insider_name": "Selipsky Adam",
          "relationship": "CEO Amazon Web Services",
          "transaction_type": "Sale",
          "price": 176.31,
          "shares": 500,
          "usd_value": 88155.0,
          "total_shares": 133100,
          "sec_form4_date": "2001-03-11",           # ISO date
          "sec_form4_datetime": "2001-03-11T16:34:00.000Z",
          "sec_form4_link": "http://www.sec.gov/..."
        }, ...
      ]
    }
    """
    obj = obj or {}
    rows = obj.get("insiderTransactions") or []
    series: List[Dict] = []
    for it in rows:
        if not isinstance(it, dict):
            continue
        date_raw = it.get("date")
        series.append(
            {
                "date": _parse_short_date(date_raw) or date_raw,
                "date_raw": date_raw,
                "insider_name": it.get("insiderTradings"),
                "relationship": it.get("relationship"),
                "transaction_type": it.get("transaction"),
                "price": to_float(it.get("cost")),
                "shares": to_int(it.get("shares")),
                "usd_value": to_float(it.get("USDValue")),
                "total_shares": to_int(it.get("totalShares")),
                "sec_form4_date": _parse_iso_date(it.get("SECForm4Date")),
                "sec_form4_datetime": it.get("SECForm4Date"),
                "sec_form4_link": it.get("SECForm4Link"),
            }
        )
    # sort ascending by the (possibly ISO) 'date' string
    series.sort(key=lambda r: r["date"] or "")
    return {"ticker": obj.get("ticker"), "name": obj.get("name"), "series": series}
