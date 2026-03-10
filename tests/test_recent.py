from finbrain_mcp.tools import recent as mod


def test_recent_news_json(patch_resolvers):
    patch_resolvers(mod)
    req = mod.RecentNewsReq(limit=10)
    out = mod.recent_news(req)
    assert out["format"] == "json"
    assert out["count"] == 2
    row = out["rows"][0]
    assert row["ticker"] == "AAPL"
    assert row["headline"] == "Apple hits new high"


def test_recent_news_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.RecentNewsReq(format="csv", limit=10)
    out = mod.recent_news(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    assert "ticker" in header
    assert "headline" in header


def test_recent_analyst_ratings_json(patch_resolvers):
    patch_resolvers(mod)
    req = mod.RecentAnalystRatingsReq(limit=10)
    out = mod.recent_analyst_ratings(req)
    assert out["format"] == "json"
    assert out["count"] == 1
    row = out["rows"][0]
    assert row["ticker"] == "AAPL"
    assert row["institution"] == "Goldman Sachs"
    assert row["rating_type"] == "Upgraded"
    assert row["signal"] == "Buy"
    assert row["target_price"] == "$250"
