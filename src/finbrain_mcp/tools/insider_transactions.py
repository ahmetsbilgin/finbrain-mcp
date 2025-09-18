from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field
from ..registry import mcp
from ..auth import resolve_api_key
from ..client_adapter import FBClient
from ..utils import latest_slice, rows_to_csv


class InsiderReq(BaseModel):
    market: str
    ticker: str
    limit: int = Field(100, ge=1, le=5000)
    format: Literal["json", "csv"] = "json"


def insider_transactions_by_ticker(req: InsiderReq):
    """
    Normalized insider transactions with paging over `series`.
    JSON:
      {
        format: "json",
        ticker, name,
        series: [{date, date_raw, insider_name, relationship, transaction_type,
                  price, shares, usd_value, total_shares,
                  sec_form4_date, sec_form4_datetime, sec_form4_link}, ...],
        series_count, series_total
      }
    CSV: sliced `series` as CSV.
    """
    client = FBClient(resolve_api_key())
    obj = client.insider_transactions_ticker(req.market, req.ticker) or {
        "ticker": req.ticker,
        "name": None,
        "series": [],
    }
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


# Register (keep function callable for tests)
mcp.tool()(insider_transactions_by_ticker)
