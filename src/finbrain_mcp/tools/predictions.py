from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, Field
from ..registry import mcp
from ..auth import resolve_api_key
from ..client_adapter import FBClient
from ..utils import latest_slice, rows_to_csv


class PredictionsScreenerReq(BaseModel):
    prediction_type: Literal["daily", "monthly"] = "daily"
    market: Optional[str] = Field(None, description="e.g., 'S&P 500'")
    region: Optional[str] = Field(None, description="e.g., 'US'")
    limit: int = Field(1000, ge=1, le=10000)
    format: Literal["json", "csv"] = "json"


class PredictionsTickerReq(BaseModel):
    ticker: str
    prediction_type: Literal["daily", "monthly"] = "daily"
    format: Literal["json", "csv"] = "json"


def predictions_by_market(req: PredictionsScreenerReq):
    """
    Screener-based market predictions (flat rows with expected_* percentages).
    Filters by market name or region.
    """
    client = FBClient(resolve_api_key())
    rows = client.screener_predictions(
        prediction_type=req.prediction_type,
        market=req.market,
        region=req.region,
        limit=req.limit,
    ) or []
    rows = latest_slice(rows, req.limit)
    if req.format == "csv":
        return {"format": "csv", "data": rows_to_csv(rows)}
    return {"format": "json", "rows": rows, "count": len(rows)}


def predictions_by_ticker(req: PredictionsTickerReq):
    """
    Normalized ticker prediction with a time series:
      {
        ticker, name, type, last_update, expected_short/mid/long,
        series: [{date, mid, low, high}, ...],
      }
    """
    client = FBClient(resolve_api_key())
    obj = client.predictions_ticker(
        req.ticker, prediction_type=req.prediction_type
    ) or {
        "ticker": req.ticker,
        "name": None,
        "series": [],
    }

    if req.format == "csv":
        return {"format": "csv", "data": rows_to_csv(obj.get("series", []))}

    return {
        "format": "json",
        "ticker": obj.get("ticker"),
        "name": obj.get("name"),
        "type": obj.get("type"),
        "last_update": obj.get("last_update"),
        "expected_short": obj.get("expected_short"),
        "expected_mid": obj.get("expected_mid"),
        "expected_long": obj.get("expected_long"),
        "series": obj.get("series", []),
        "series_total": len(obj.get("series", [])),
    }


# Keep functions callable in tests but register them for MCP
mcp.tool()(predictions_by_market)
mcp.tool()(predictions_by_ticker)
