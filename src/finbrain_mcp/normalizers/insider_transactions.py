from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_float, to_int


def normalize_insider_transactions_ticker(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "AMZN",
      "name": "Amazon.com Inc.",
      "transactions": [
        {
          "date": "2024-03-08",
          "insider": "Selipsky Adam",
          "relationship": "CEO Amazon Web Services",
          "transactionType": "Sale",
          "shares": 500,
          "pricePerShare": 176.31,
          "totalValue": 88155,
          "sharesOwned": 133100,
          "filingDate": "2024-03-11",
          "filingUrl": "http://www.sec.gov/..."
        }, ...
      ]
    }

    -> {
      "ticker": "AMZN", "name": "...",
      "series": [
        {
          "date": "2024-03-08",
          "insider_name": "Selipsky Adam",
          "relationship": "CEO Amazon Web Services",
          "transaction_type": "Sale",
          "price": 176.31,
          "shares": 500,
          "usd_value": 88155.0,
          "total_shares": 133100,
          "sec_form4_date": "2024-03-11",
          "sec_form4_link": "http://www.sec.gov/..."
        }, ...
      ]
    }
    """
    obj = obj or {}
    rows = obj.get("transactions") or []
    series: List[Dict] = []
    for it in rows:
        if not isinstance(it, dict):
            continue
        series.append(
            {
                "date": it.get("date"),
                "insider_name": it.get("insider"),
                "relationship": it.get("relationship"),
                "transaction_type": it.get("transactionType"),
                "price": to_float(it.get("pricePerShare")),
                "shares": to_int(it.get("shares")),
                "usd_value": to_float(it.get("totalValue")),
                "total_shares": to_int(it.get("sharesOwned")),
                "sec_form4_date": it.get("filingDate"),
                "sec_form4_link": it.get("filingUrl"),
            }
        )
    series.sort(key=lambda r: r["date"] or "")
    return {"ticker": obj.get("symbol"), "name": obj.get("name"), "series": series}
