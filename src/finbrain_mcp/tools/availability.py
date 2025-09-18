from __future__ import annotations
from typing import Literal
from pydantic import BaseModel
from ..registry import mcp
from ..auth import resolve_api_key
from ..client_adapter import FBClient


class TickersReq(BaseModel):
    dataset: Literal["daily", "monthly"] = "daily"
    format: Literal["json"] = "json"  # only json for this one


def available_markets() -> list[str] | dict:
    """List available markets (e.g., 'S&P 500')."""
    client = FBClient(resolve_api_key())
    return client.available_markets()


def available_tickers(req: TickersReq):
    """List available tickers for a dataset."""
    client = FBClient(resolve_api_key())
    return client.available_tickers(req.dataset)


mcp.tool()(available_markets)
mcp.tool()(available_tickers)
