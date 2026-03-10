from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, Field
from ..registry import mcp
from ..auth import resolve_api_key
from ..client_adapter import FBClient
from ..utils import latest_slice, rows_to_csv


class RecentNewsReq(BaseModel):
    market: Optional[str] = Field(None, description="e.g., 'S&P 500'")
    region: Optional[str] = Field(None, description="e.g., 'US'")
    limit: int = Field(100, ge=1, le=20000)
    format: Literal["json", "csv"] = "json"


class RecentAnalystRatingsReq(BaseModel):
    market: Optional[str] = Field(None, description="e.g., 'S&P 500'")
    region: Optional[str] = Field(None, description="e.g., 'US'")
    limit: int = Field(100, ge=1, le=20000)
    format: Literal["json", "csv"] = "json"


def recent_news(req: RecentNewsReq):
    """
    Get the most recent news articles across all tracked stocks.
    Returns rows with ticker, name, date, headline, source, url.
    """
    client = FBClient(resolve_api_key())
    rows = client.recent_news(
        limit=req.limit, market=req.market, region=req.region
    ) or []
    rows = latest_slice(rows, req.limit)
    if req.format == "csv":
        return {"format": "csv", "data": rows_to_csv(rows)}
    return {"format": "json", "rows": rows, "count": len(rows)}


def recent_analyst_ratings(req: RecentAnalystRatingsReq):
    """
    Get the most recent analyst ratings across all tracked stocks.
    Returns rows with ticker, name, date, institution, rating_type, signal, target_price.
    """
    client = FBClient(resolve_api_key())
    rows = client.recent_analyst_ratings(
        limit=req.limit, market=req.market, region=req.region
    ) or []
    rows = latest_slice(rows, req.limit)
    if req.format == "csv":
        return {"format": "csv", "data": rows_to_csv(rows)}
    return {"format": "json", "rows": rows, "count": len(rows)}


mcp.tool()(recent_news)
mcp.tool()(recent_analyst_ratings)
