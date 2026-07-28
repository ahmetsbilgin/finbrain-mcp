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
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "META",
      "name": "Meta Platforms Inc.",
      "chamber": "senate",
      "trades": [
        {"date": "2025-11-13", "politician": "Shelley Moore Capito",
         "transactionType": "Purchase", "amount": "$1,001 - $15,000",
         "owner": "SP", "amountRaw": None, "amountFlag": None,
         "disclosureDate": "2025-12-04"},
        ...
      ]
    }

    -> {
      "ticker": "META",
      "name": "...",
      "series": [
        {"date": "2025-11-13", "senator": "Shelley Moore Capito",
         "trade_type": "Purchase",
         "amount_min": 1001.0, "amount_max": 15000.0,
         "amount_exact": False, "amount_raw": "$1,001 - $15,000",
         "disclosure_date": "2025-12-04",
         "owner": "SP", "amount_as_filed": None, "amount_flag": None},
        ...
      ]
    }

    ``disclosure_date`` is the date the trade was publicly disclosed in the
    member's periodic transaction report; ``date`` is when the trade was
    executed. The gap between them is the reporting lag.

    ``owner`` is the beneficial owner of the traded account: "SELF", "SP"
    (spouse), "DC" (dependent child), "JT" (joint), an account code, or
    "UNKNOWN" for Senate filings that leave the owner column blank.
    ``owner`` and ``disclosure_date`` are nullable; historical rows were
    backfilled upstream, so nulls are rare but possible.

    ``amount_raw`` is the amount string as served by the API, which
    normalizes it to a statutory STOCK Act bracket whenever the filed
    string is an unambiguous formatting variant of one. On normalized rows
    ``amount_as_filed`` (the API's ``amountRaw``) preserves the string as
    originally filed. When the filed amount could not be safely normalized,
    ``amount_raw`` keeps the filed string (or "Unknown" when the filing had
    no usable amount) and ``amount_flag`` (the API's ``amountFlag``) is
    "review" or "ambiguous"; on all other rows both are ``None``.
    """
    obj = obj or {}
    rows = obj.get("trades") or []
    series: List[Dict] = []
    for it in rows:
        if not isinstance(it, dict):
            continue
        mn, mx, exact = _parse_amount(it.get("amount"))
        series.append(
            {
                "date": it.get("date"),
                "senator": it.get("politician"),
                "trade_type": it.get("transactionType"),
                "amount_min": mn,
                "amount_max": mx,
                "amount_exact": exact,
                "amount_raw": it.get("amount"),
                "disclosure_date": it.get("disclosureDate"),
                "owner": it.get("owner"),
                "amount_as_filed": it.get("amountRaw"),
                "amount_flag": it.get("amountFlag"),
            }
        )
    series.sort(key=lambda r: r["date"])
    return {"ticker": obj.get("symbol"), "name": obj.get("name"), "series": series}
