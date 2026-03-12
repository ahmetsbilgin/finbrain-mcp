from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, Field
from ..registry import mcp
from ..auth import resolve_api_key
from ..client_adapter import FBClient
from ..utils import latest_slice, rows_to_csv


class CorporateLobbyingReq(BaseModel):
    ticker: str
    date_from: Optional[str] = Field(None, description="YYYY-MM-DD")
    date_to: Optional[str] = Field(None, description="YYYY-MM-DD")
    limit: int = Field(100, ge=1, le=5000)
    format: Literal["json", "csv"] = "json"


def corporate_lobbying_by_ticker(req: CorporateLobbyingReq):
    """
    Normalized corporate lobbying filings:
      {
        format: "json",
        ticker, name,
        series: [{date, filing_uuid, filing_year, quarter,
                  client_name, registrant_name,
                  income, expenses, issue_codes, government_entities}, ...],
        series_count, series_total
      }
    CSV returns the sliced `series`.
    """
    client = FBClient(resolve_api_key())
    obj = client.corporate_lobbying_ticker(
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
mcp.tool()(corporate_lobbying_by_ticker)
