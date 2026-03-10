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
    assert any(row.get("symbol") == "AMZN" for row in out)


def test_available_regions(patch_resolvers):
    patch_resolvers(mod)
    regions = mod.available_regions()
    assert isinstance(regions, list)
    assert any(r.get("region") == "US" for r in regions)
    us = next(r for r in regions if r["region"] == "US")
    assert "S&P 500" in us["markets"]
