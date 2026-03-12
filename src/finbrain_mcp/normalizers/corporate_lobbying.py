from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_float, to_int


def normalize_corporate_lobbying_ticker(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "filings": [
        {"date": "2024-03-15", "filingUuid": "abc-123", "filingYear": 2024,
         "quarter": "Q1", "clientName": "Apple Inc.",
         "registrantName": "Lobbying Firm LLC",
         "income": 50000, "expenses": 75000,
         "issueCodes": ["TAX", "ITC"],
         "governmentEntities": ["Congress", "Senate"]},
        ...
      ]
    }

    -> {
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "series": [
        {"date": "2024-03-15", "filing_uuid": "abc-123", "filing_year": 2024,
         "quarter": "Q1", "client_name": "Apple Inc.",
         "registrant_name": "Lobbying Firm LLC",
         "income": 50000.0, "expenses": 75000.0,
         "issue_codes": ["TAX", "ITC"],
         "government_entities": ["Congress", "Senate"]},
        ...
      ]
    }
    """
    obj = obj or {}
    rows = obj.get("filings") or []
    series: List[Dict] = []
    for it in rows:
        if not isinstance(it, dict):
            continue
        series.append(
            {
                "date": it.get("date"),
                "filing_uuid": it.get("filingUuid"),
                "filing_year": to_int(it.get("filingYear")),
                "quarter": it.get("quarter"),
                "client_name": it.get("clientName"),
                "registrant_name": it.get("registrantName"),
                "income": to_float(it.get("income")),
                "expenses": to_float(it.get("expenses")),
                "issue_codes": it.get("issueCodes") or [],
                "government_entities": it.get("governmentEntities") or [],
            }
        )
    series.sort(key=lambda r: r["date"] or "")
    return {"ticker": obj.get("symbol"), "name": obj.get("name"), "series": series}
