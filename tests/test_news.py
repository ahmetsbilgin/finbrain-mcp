from finbrain_mcp.tools import news as mod


def test_news_by_ticker_json(patch_resolvers):
    patch_resolvers(mod)
    req = mod.NewsReq(ticker="AMZN", limit=5)
    out = mod.news_by_ticker(req)
    assert out["format"] == "json"
    assert out["ticker"] == "AMZN"
    assert out["series_total"] == 2
    rows = out["series"]
    # sorted by date ascending
    assert rows[0]["date"] == "2026-01-18"
    assert rows[1]["date"] == "2026-01-19"
    assert rows[0]["headline"] == "Analyst raises price target"
    assert rows[0]["source"] == "Bloomberg"
    assert rows[0]["url"] == "https://example.com/article2"


def test_news_by_ticker_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.NewsReq(ticker="AMZN", format="csv", limit=5)
    out = mod.news_by_ticker(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    for col in ["date", "headline", "source", "url"]:
        assert col in header
