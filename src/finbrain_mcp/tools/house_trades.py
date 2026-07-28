from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, Field
from ..registry import mcp
from ..auth import resolve_api_key
from ..client_adapter import FBClient
from ..utils import latest_slice, rows_to_csv


class HouseTradesReq(BaseModel):
    ticker: str
    date_from: Optional[str] = Field(
        None, description="YYYY-MM-DD; bounds the transaction date, not disclosure_date"
    )
    date_to: Optional[str] = Field(
        None, description="YYYY-MM-DD; bounds the transaction date, not disclosure_date"
    )
    limit: int = Field(100, ge=1, le=5000)
    format: Literal["json", "csv"] = "json"


def house_trades_by_ticker(req: HouseTradesReq):
    """
    Normalized US House trades:
      {
        format: "json",
        ticker, name,
        series: [{date, representative, trade_type,
                  amount_min, amount_max, amount_exact, amount_raw,
                  disclosure_date, owner, amount_as_filed, amount_flag}, ...],
        series_count, series_total
      }
    `date` is the transaction date; `disclosure_date` is when the trade was
    publicly disclosed in the member's periodic transaction report. The gap
    between them is the reporting lag.
    `owner` is the beneficial owner of the traded account: "SELF", "SP"
    (spouse), "DC" (dependent child), "JT" (joint), or an account code;
    blank House filings report as "SELF". `owner` and `disclosure_date` are
    nullable, though rare — historical rows were backfilled upstream.
    `amount_raw` is the amount string as served by the API, normalized to a
    statutory STOCK Act bracket when the filed string is an unambiguous
    variant of one; `amount_as_filed` then preserves the original filing.
    `amount_flag` is "review" or "ambiguous" when the filed amount could not
    be safely normalized (amount_raw keeps the filed string, or "Unknown");
    both are null on all other rows.
    CSV returns the sliced `series`.
    """
    client = FBClient(resolve_api_key())
    obj = client.house_trades_ticker(
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
mcp.tool()(house_trades_by_ticker)
