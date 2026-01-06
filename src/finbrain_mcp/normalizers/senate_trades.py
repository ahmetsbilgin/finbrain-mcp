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


def normalize_senate_trades_ticker(obj: Any) -> Dict:
    """
    RAW:
    {
      "ticker": "META",
      "name": "Meta Platforms Inc.",
      "senateTrades": [
        {"date":"2025-11-13","amount":"$1,001 - $15,000","senator":"Shelley Moore Capito","type":"Purchase"},
        {"date":"2025-10-31","amount":"$1,001 - $15,000","senator":"John Boozman","type":"Purchase"},
        ...
      ]
    }

    -> {
      "ticker": "META",
      "name": "...",
      "series": [
        {"date":"2025-10-31","senator":"John Boozman","trade_type":"Purchase",
         "amount_min":1001.0,"amount_max":15000.0,"amount_exact":False,"amount_raw":"$1,001 - $15,000"},
        {"date":"2025-11-13","senator":"Shelley Moore Capito","trade_type":"Purchase",
         "amount_min":1001.0,"amount_max":15000.0,"amount_exact":False,"amount_raw":"$1,001 - $15,000"},
        ...
      ]
    }
    """
    obj = obj or {}
    rows = obj.get("senateTrades") or []
    series: List[Dict] = []
    for it in rows:
        if not isinstance(it, dict):
            continue
        mn, mx, exact = _parse_amount(it.get("amount"))
        series.append(
            {
                "date": it.get("date"),
                "senator": it.get("senator"),
                "trade_type": it.get("type"),
                "amount_min": mn,
                "amount_max": mx,
                "amount_exact": exact,
                "amount_raw": it.get("amount"),
            }
        )
    series.sort(key=lambda r: r["date"])
    return {"ticker": obj.get("ticker"), "name": obj.get("name"), "series": series}
