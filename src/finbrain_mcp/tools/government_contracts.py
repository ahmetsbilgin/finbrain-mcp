from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, Field
from ..registry import mcp
from ..auth import resolve_api_key
from ..client_adapter import FBClient
from ..utils import latest_slice, rows_to_csv


class GovernmentContractsReq(BaseModel):
    ticker: str
    date_from: Optional[str] = Field(None, description="YYYY-MM-DD")
    date_to: Optional[str] = Field(None, description="YYYY-MM-DD")
    limit: int = Field(100, ge=1, le=5000)
    format: Literal["json", "csv"] = "json"


def government_contracts_by_ticker(req: GovernmentContractsReq):
    """
    U.S. government contract awards for a single ticker:
      {
        format: "json",
        ticker, name,
        series: [{award_id, award_amount, award_type, awarding_agency,
                  awarding_sub_agency, recipient_name, start_date, end_date,
                  description, naics_code, naics_description,
                  contract_award_type}, ...],
        series_count, series_total
      }
    CSV returns the sliced `series`.
    """
    client = FBClient(resolve_api_key())
    obj = client.government_contracts_ticker(
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
mcp.tool()(government_contracts_by_ticker)
