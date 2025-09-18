from finbrain_mcp.tools import sentiments as mod


def test_news_sentiment_json_series(patch_resolvers):
    patch_resolvers(mod)
    req = mod.SentimentsReq(market="S&P 500", ticker="AMZN", limit=2)
    out = mod.news_sentiment_by_ticker(req)
    assert out["format"] == "json"
    assert out["ticker"] == "AMZN"
    assert out["series_count"] == 2
    assert out["series_total"] == 3
    # ascending by date: first two should be 13th and 14th
    dates = [r["date"] for r in out["series"]]
    assert dates == ["2021-12-14", "2021-12-15"]
    assert "score" in out["series"][0]
    assert isinstance(out["series"][0]["score"], float)


def test_news_sentiment_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.SentimentsReq(market="S&P 500", ticker="AMZN", format="csv", limit=1)
    out = mod.news_sentiment_by_ticker(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    assert "date" in header and "score" in header
