from finbrain_mcp.tools import availability as mod


def test_available_markets(patch_resolvers):
    patch_resolvers(mod)
    markets = mod.available_markets()
    assert isinstance(markets, list)
    assert "S&P 500" in markets


def test_available_tickers(patch_resolvers):
    patch_resolvers(mod)
    req = mod.TickersReq(dataset="daily")
    out = mod.available_tickers(req)
    assert isinstance(out, list)
    assert any(row.get("ticker") == "AMZN" for row in out)
