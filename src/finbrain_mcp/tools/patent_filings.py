from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, Field
from ..registry import mcp
from ..auth import resolve_api_key
from ..client_adapter import FBClient
from ..utils import latest_slice, rows_to_csv


class PatentFilingsReq(BaseModel):
    ticker: str
    date_from: Optional[str] = Field(None, description="YYYY-MM-DD")
    date_to: Optional[str] = Field(None, description="YYYY-MM-DD")
    limit: int = Field(100, ge=1, le=5000)
    format: Literal["json", "csv"] = "json"


def patent_filings_by_ticker(req: PatentFilingsReq):
    """
    USPTO granted patents mapped to a single ticker by corporate assignee:
      {
        format: "json",
        ticker, name,
        series: [{patent_id, patent_date, title, type, kind, num_claims,
                  num_cited_by, assignee_organization, assignee_type,
                  application_filing_date, filing_to_grant_days, inventors,
                  num_inventors, cpc_sections, cpc_subsections,
                  primary_cpc_section}, ...],
        series_count, series_total
      }
    CSV returns the sliced `series`.
    """
    client = FBClient(resolve_api_key())
    obj = client.patent_filings_ticker(
        req.ticker, req.date_from, req.date_to
    ) or {"ticker": req.ticker, "name": None, "series": []}
    series = obj.get("series", [])
    series_slice = latest_slice(series, req.limit)

    if req.format == "csv":
        return {"format": "csv", "data": rows_to_csv(series_slice)}

    return {
        "format": "json",
        "ticker": obj.get("ticker"),
        "name": obj.get("name"),
        "series": series_slice,
        "series_count": len(series_slice),
        "series_total": len(series),
    }


# Register with MCP while keeping function callable for tests
mcp.tool()(patent_filings_by_ticker)
