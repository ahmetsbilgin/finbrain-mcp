from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_float, to_int


def normalize_government_contracts_ticker(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "LMT",
      "name": "Lockheed Martin Corporation",
      "contracts": [
        {"awardId": "CONT_AWD_0001", "awardAmount": 50000000,
         "awardType": "", "awardingAgency": "Department of Defense",
         "awardingSubAgency": "Department of the Army",
         "recipientName": "Lockheed Martin Corporation",
         "startDate": "2025-06-01", "endDate": "2026-06-01",
         "description": "Aircraft maintenance services",
         "naicsCode": "336411", "naicsDescription": "Aircraft Manufacturing",
         "contractAwardType": ""},
        ...
      ]
    }

    -> {
      "ticker": "LMT",
      "name": "Lockheed Martin Corporation",
      "series": [
        {"award_id": "CONT_AWD_0001", "award_amount": 50000000.0,
         "award_type": "", "awarding_agency": "Department of Defense",
         "awarding_sub_agency": "Department of the Army",
         "recipient_name": "Lockheed Martin Corporation",
         "start_date": "2025-06-01", "end_date": "2026-06-01",
         "description": "Aircraft maintenance services",
         "naics_code": "336411", "naics_description": "Aircraft Manufacturing",
         "contract_award_type": ""},
        ...
      ]
    }
    """
    obj = obj or {}
    rows = obj.get("contracts") or []
    series: List[Dict] = []
    for it in rows:
        if not isinstance(it, dict):
            continue
        series.append(
            {
                "award_id": it.get("awardId"),
                "award_amount": to_float(it.get("awardAmount")),
                "award_type": it.get("awardType") or "",
                "awarding_agency": it.get("awardingAgency"),
                "awarding_sub_agency": it.get("awardingSubAgency"),
                "recipient_name": it.get("recipientName"),
                "start_date": it.get("startDate"),
                "end_date": it.get("endDate"),
                "description": it.get("description"),
                "naics_code": it.get("naicsCode"),
                "naics_description": it.get("naicsDescription"),
                "contract_award_type": it.get("contractAwardType") or "",
            }
        )
    series.sort(key=lambda r: r["start_date"] or "")
    return {"ticker": obj.get("symbol"), "name": obj.get("name"), "series": series}


def normalize_screener_government_contracts(items: Any) -> List[Dict]:
    """
    V2 screener government contracts rows.
    [{symbol, name, awardId, awardAmount, recipientName, startDate,
      awardingAgency, naicsDescription}]
    -> [{ticker, name, award_id, award_amount, recipient_name, start_date,
        awarding_agency, naics_description}]
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
                "award_id": it.get("awardId"),
                "award_amount": to_float(it.get("awardAmount")),
                "recipient_name": it.get("recipientName"),
                "start_date": it.get("startDate"),
                "awarding_agency": it.get("awardingAgency"),
                "naics_description": it.get("naicsDescription"),
            }
        )
    return out


def normalize_screener_government_contracts_summary(summary: Any) -> Dict:
    """
    {totalContracts, totalTickers, totalValue}
    -> {total_contracts, total_tickers, total_value}
    """
    summary = summary or {}
    return {
        "total_contracts": to_int(summary.get("totalContracts")),
        "total_tickers": to_int(summary.get("totalTickers")),
        "total_value": to_float(summary.get("totalValue")),
    }
