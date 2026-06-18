from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, Field
from ..registry import mcp
from ..auth import resolve_api_key
from ..client_adapter import FBClient
from ..utils import latest_slice, rows_to_csv


# ---------- request models ----------

class ScreenerMarketReq(BaseModel):
    """Screener request requiring market or region."""
    market: Optional[str] = Field(None, description="e.g., 'S&P 500' (market or region required)")
    region: Optional[str] = Field(None, description="e.g., 'US' (market or region required)")
    limit: int = Field(1000, ge=1, le=20000)
    format: Literal["json", "csv"] = "json"


class ScreenerOptionalMarketReq(BaseModel):
    """Screener request with optional market/region."""
    market: Optional[str] = Field(None, description="e.g., 'S&P 500'")
    region: Optional[str] = Field(None, description="e.g., 'US'")
    limit: int = Field(1000, ge=1, le=20000)
    format: Literal["json", "csv"] = "json"


class ScreenerLimitOnlyReq(BaseModel):
    """Screener request with limit only (no market/region filter)."""
    limit: int = Field(1000, ge=1, le=20000)
    format: Literal["json", "csv"] = "json"


# ---------- helper ----------

def _screener_response(rows: list, limit: int, fmt: str) -> dict:
    rows = latest_slice(rows, limit)
    if fmt == "csv":
        return {"format": "csv", "data": rows_to_csv(rows)}
    return {"format": "json", "rows": rows, "count": len(rows)}


# ---------- tools ----------

def screener_sentiment(req: ScreenerMarketReq):
    """
    Screen sentiment across tickers by market or region.
    Returns rows with ticker, name, date, score.
    Either market or region is required.
    """
    client = FBClient(resolve_api_key())
    rows = client.screener_sentiment(
        market=req.market, region=req.region, limit=req.limit
    ) or []
    return _screener_response(rows, req.limit, req.format)


def screener_analyst_ratings(req: ScreenerOptionalMarketReq):
    """
    Screen analyst ratings across tickers.
    Returns rows with ticker, name, date, institution, rating_type, signal, target_price.
    """
    client = FBClient(resolve_api_key())
    rows = client.screener_analyst_ratings(
        market=req.market, region=req.region, limit=req.limit
    ) or []
    return _screener_response(rows, req.limit, req.format)


def screener_insider_trading(req: ScreenerLimitOnlyReq):
    """
    Screen insider trades across all tickers.
    Returns rows with ticker, name, date, insider_name, relationship,
    transaction_type, shares, total_value.
    """
    client = FBClient(resolve_api_key())
    rows = client.screener_insider_trading(limit=req.limit) or []
    return _screener_response(rows, req.limit, req.format)


def screener_house_trades(req: ScreenerLimitOnlyReq):
    """
    Screen House of Representatives trades across all tickers.
    Returns rows with ticker, name, date, politician, trade_type, amount.
    """
    client = FBClient(resolve_api_key())
    rows = client.screener_congress_house(limit=req.limit) or []
    return _screener_response(rows, req.limit, req.format)


def screener_senate_trades(req: ScreenerLimitOnlyReq):
    """
    Screen Senate trades across all tickers.
    Returns rows with ticker, name, date, politician, trade_type, amount.
    """
    client = FBClient(resolve_api_key())
    rows = client.screener_congress_senate(limit=req.limit) or []
    return _screener_response(rows, req.limit, req.format)


def screener_news(req: ScreenerOptionalMarketReq):
    """
    Screen news across tickers.
    Returns rows with ticker, name, date, headline, source, url.
    """
    client = FBClient(resolve_api_key())
    rows = client.screener_news(
        market=req.market, region=req.region, limit=req.limit
    ) or []
    return _screener_response(rows, req.limit, req.format)


def screener_put_call_ratio(req: ScreenerOptionalMarketReq):
    """
    Screen put/call ratio across tickers.
    Returns rows with ticker, name, date, put_call_ratio, call_count, put_count.
    """
    client = FBClient(resolve_api_key())
    rows = client.screener_put_call_ratio(
        market=req.market, region=req.region, limit=req.limit
    ) or []
    return _screener_response(rows, req.limit, req.format)


def screener_linkedin(req: ScreenerMarketReq):
    """
    Screen LinkedIn data across tickers by market or region.
    Returns rows with ticker, name, date, employee_count, followers_count, job_count.
    Either market or region is required.
    """
    client = FBClient(resolve_api_key())
    rows = client.screener_linkedin(
        market=req.market, region=req.region, limit=req.limit
    ) or []
    return _screener_response(rows, req.limit, req.format)


def screener_app_ratings(req: ScreenerMarketReq):
    """
    Screen app ratings across tickers by market or region.
    Returns rows with ticker, name, date, app_store_score, play_store_score.
    Either market or region is required.
    """
    client = FBClient(resolve_api_key())
    rows = client.screener_app_ratings(
        market=req.market, region=req.region, limit=req.limit
    ) or []
    return _screener_response(rows, req.limit, req.format)


def screener_government_contracts(req: ScreenerLimitOnlyReq):
    """
    Screen U.S. government contract awards across all tickers.
    Returns rows with ticker, name, award_id, award_amount, recipient_name,
    start_date, awarding_agency, naics_description,
    plus a summary with aggregate stats (total_contracts, total_tickers, total_value).
    """
    client = FBClient(resolve_api_key())
    result = client.screener_government_contracts(
        limit=req.limit
    ) or {"rows": [], "summary": {}}
    rows = result.get("rows", [])
    resp = _screener_response(rows, req.limit, req.format)
    if resp["format"] == "json":
        resp["summary"] = result.get("summary", {})
    return resp


def screener_patent_filings(req: ScreenerLimitOnlyReq):
    """
    Screen USPTO granted patents across all tickers.
    Returns rows with ticker, name, patent_id, patent_date, title, type,
    assignee_organization, primary_cpc_section, num_claims,
    plus a summary with aggregate stats (total_patents, total_tickers, top_cpc_sections).
    """
    client = FBClient(resolve_api_key())
    result = client.screener_patent_filings(
        limit=req.limit
    ) or {"rows": [], "summary": {}}
    rows = result.get("rows", [])
    resp = _screener_response(rows, req.limit, req.format)
    if resp["format"] == "json":
        resp["summary"] = result.get("summary", {})
    return resp


def screener_reddit_mentions(req: ScreenerOptionalMarketReq):
    """
    Screen Reddit mentions across tickers.
    Returns rows with ticker, name, date, total_mentions, subreddits,
    plus a summary with aggregate stats (top_mentioned, subreddit_names, etc.).
    """
    client = FBClient(resolve_api_key())
    result = client.screener_reddit_mentions(
        market=req.market, region=req.region, limit=req.limit
    ) or {"rows": [], "summary": {}}
    rows = result.get("rows", [])
    resp = _screener_response(rows, req.limit, req.format)
    if resp["format"] == "json":
        resp["summary"] = result.get("summary", {})
    return resp


# Register all tools with MCP
mcp.tool()(screener_sentiment)
mcp.tool()(screener_analyst_ratings)
mcp.tool()(screener_insider_trading)
mcp.tool()(screener_house_trades)
mcp.tool()(screener_senate_trades)
mcp.tool()(screener_news)
mcp.tool()(screener_put_call_ratio)
mcp.tool()(screener_linkedin)
mcp.tool()(screener_app_ratings)
mcp.tool()(screener_government_contracts)
mcp.tool()(screener_patent_filings)
mcp.tool()(screener_reddit_mentions)
