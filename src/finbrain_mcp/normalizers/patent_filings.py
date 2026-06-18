from __future__ import annotations
from typing import Any, Dict, List
from .shared import to_int


def _to_str_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(v) for v in value if v is not None]
    return []


def normalize_patent_filings_ticker(obj: Any) -> Dict:
    """
    V2 RAW (after SDK envelope unwrap):
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "patents": [
        {"patentId": "12345678", "patentDate": "2025-06-01",
         "title": "Method and apparatus for on-device machine learning",
         "type": "utility", "kind": "B2", "numClaims": 20, "numCitedBy": 5,
         "assigneeOrganization": "Apple Inc.", "assigneeType": "2",
         "applicationFilingDate": "2022-03-15", "filingToGrantDays": 808,
         "inventors": ["Jane Doe", "John Roe"], "numInventors": 2,
         "cpcSections": ["G", "H"], "cpcSubsections": ["G06", "H04"],
         "primaryCpcSection": "G"},
        ...
      ]
    }

    -> {
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "series": [
        {"patent_id": "12345678", "patent_date": "2025-06-01",
         "title": "Method and apparatus for on-device machine learning",
         "type": "utility", "kind": "B2", "num_claims": 20, "num_cited_by": 5,
         "assignee_organization": "Apple Inc.", "assignee_type": "2",
         "application_filing_date": "2022-03-15", "filing_to_grant_days": 808,
         "inventors": ["Jane Doe", "John Roe"], "num_inventors": 2,
         "cpc_sections": ["G", "H"], "cpc_subsections": ["G06", "H04"],
         "primary_cpc_section": "G"},
        ...
      ]
    }
    """
    obj = obj or {}
    rows = obj.get("patents") or []
    series: List[Dict] = []
    for it in rows:
        if not isinstance(it, dict):
            continue
        series.append(
            {
                "patent_id": it.get("patentId"),
                "patent_date": it.get("patentDate"),
                "title": it.get("title"),
                "type": it.get("type") or "",
                "kind": it.get("kind") or "",
                "num_claims": to_int(it.get("numClaims")),
                "num_cited_by": to_int(it.get("numCitedBy")),
                "assignee_organization": it.get("assigneeOrganization"),
                "assignee_type": it.get("assigneeType") or "",
                "application_filing_date": it.get("applicationFilingDate"),
                "filing_to_grant_days": to_int(it.get("filingToGrantDays")),
                "inventors": _to_str_list(it.get("inventors")),
                "num_inventors": to_int(it.get("numInventors")),
                "cpc_sections": _to_str_list(it.get("cpcSections")),
                "cpc_subsections": _to_str_list(it.get("cpcSubsections")),
                "primary_cpc_section": it.get("primaryCpcSection") or "",
            }
        )
    series.sort(key=lambda r: r["patent_date"] or "")
    return {"ticker": obj.get("symbol"), "name": obj.get("name"), "series": series}


def normalize_screener_patent_filings(items: Any) -> List[Dict]:
    """
    V2 screener patent filings rows.
    [{symbol, name, patentId, patentDate, title, type,
      assigneeOrganization, primaryCpcSection, numClaims}]
    -> [{ticker, name, patent_id, patent_date, title, type,
        assignee_organization, primary_cpc_section, num_claims}]
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
                "patent_id": it.get("patentId"),
                "patent_date": it.get("patentDate"),
                "title": it.get("title"),
                "type": it.get("type") or "",
                "assignee_organization": it.get("assigneeOrganization"),
                "primary_cpc_section": it.get("primaryCpcSection") or "",
                "num_claims": to_int(it.get("numClaims")),
            }
        )
    return out


def normalize_screener_patent_filings_summary(summary: Any) -> Dict:
    """
    {totalPatents, totalTickers, topCpcSections}
    -> {total_patents, total_tickers, top_cpc_sections}
    """
    summary = summary or {}
    top = summary.get("topCpcSections")
    return {
        "total_patents": to_int(summary.get("totalPatents")),
        "total_tickers": to_int(summary.get("totalTickers")),
        "top_cpc_sections": _to_str_list(top),
    }
