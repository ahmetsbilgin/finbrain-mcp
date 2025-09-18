from __future__ import annotations
from typing import Any, Dict, List, Tuple
import re

_amount_re = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")


def _parse_amount(s: Any) -> Tuple[float | None, float | None, bool]:
    """
    Parse strings like:
      "$360.00" -> (360.0, 360.0, True)
      "$15,001 - $50,000" -> (15001.0, 50000.0, False)
      "Over $50,000,000" -> (50000000.0, None, False)
    Returns (min, max, exact).
    """
    if s is None:
        return (None, None, False)
    text = str(s)
    nums = [float(n.replace(",", "")) for n in _amount_re.findall(text)]
    low_text = text.lower()
    if ("over" in low_text or "more than" in low_text) and nums:
        return (nums[0], None, False)
    if len(nums) >= 2:
        return (nums[0], nums[1], False)
    if len(nums) == 1:
        return (nums[0], nums[0], True)
    return (None, None, False)


def normalize_house_trades_ticker(obj: Any) -> Dict:
    """
    RAW:
    {
      "ticker": "AMZN",
      "name": "Amazon.com Inc.",
      "houseTrades": [
        {"date":"2024-02-29","amount":"$360.00","representative":"Pete Sessions","type":"Purchase"},
        {"date":"2024-01-25","amount":"$15,001 - $50,000","representative":"Shri Thanedar","type":"Sale"},
        ...
      ]
    }

    -> {
      "ticker": "AMZN",
      "name": "...",
      "series": [
        {"date":"2024-01-25","representative":"Shri Thanedar","trade_type":"Sale",
         "amount_min":15001.0,"amount_max":50000.0,"amount_exact":False,"amount_raw":"$15,001 - $50,000"},
        {"date":"2024-02-29","representative":"Pete Sessions","trade_type":"Purchase",
         "amount_min":360.0,"amount_max":360.0,"amount_exact":True,"amount_raw":"$360.00"},
        ...
      ]
    }
    """
    obj = obj or {}
    rows = obj.get("houseTrades") or []
    series: List[Dict] = []
    for it in rows:
        if not isinstance(it, dict):
            continue
        mn, mx, exact = _parse_amount(it.get("amount"))
        series.append(
            {
                "date": it.get("date"),
                "representative": it.get("representative"),
                "trade_type": it.get("type"),
                "amount_min": mn,
                "amount_max": mx,
                "amount_exact": exact,
                "amount_raw": it.get("amount"),
            }
        )
    series.sort(key=lambda r: r["date"])
    return {"ticker": obj.get("ticker"), "name": obj.get("name"), "series": series}
