from finbrain_mcp.tools import screener as mod


def test_screener_sentiment(patch_resolvers):
    patch_resolvers(mod)
    req = mod.ScreenerMarketReq(market="S&P 500")
    out = mod.screener_sentiment(req)
    assert out["format"] == "json"
    assert out["count"] == 2
    row = out["rows"][0]
    assert row["ticker"] == "AAPL"
    assert row["score"] == 0.45


def test_screener_analyst_ratings(patch_resolvers):
    patch_resolvers(mod)
    req = mod.ScreenerOptionalMarketReq(region="US")
    out = mod.screener_analyst_ratings(req)
    assert out["count"] == 1
    row = out["rows"][0]
    assert row["ticker"] == "AAPL"
    assert row["institution"] == "Morgan Stanley"
    assert row["rating_type"] == "Reiterated"
    assert row["signal"] == "Overweight"


def test_screener_insider_trading(patch_resolvers):
    patch_resolvers(mod)
    req = mod.ScreenerLimitOnlyReq(limit=10)
    out = mod.screener_insider_trading(req)
    assert out["count"] == 1
    row = out["rows"][0]
    assert row["ticker"] == "AMZN"
    assert row["insider_name"] == "Jassy Andrew R"
    assert row["transaction_type"] == "Sale"
    assert row["shares"] == 5000
    assert row["total_value"] == 950000


def test_screener_house_trades(patch_resolvers):
    patch_resolvers(mod)
    req = mod.ScreenerLimitOnlyReq(limit=10)
    out = mod.screener_house_trades(req)
    assert out["count"] == 1
    row = out["rows"][0]
    assert row["ticker"] == "NVDA"
    assert row["politician"] == "Nancy Pelosi"
    assert row["trade_type"] == "Purchase"


def test_screener_senate_trades(patch_resolvers):
    patch_resolvers(mod)
    req = mod.ScreenerLimitOnlyReq(limit=10)
    out = mod.screener_senate_trades(req)
    assert out["count"] == 1
    row = out["rows"][0]
    assert row["ticker"] == "MSFT"
    assert row["politician"] == "Tommy Tuberville"


def test_screener_news(patch_resolvers):
    patch_resolvers(mod)
    req = mod.ScreenerOptionalMarketReq(limit=10)
    out = mod.screener_news(req)
    assert out["count"] == 1
    row = out["rows"][0]
    assert row["ticker"] == "TSLA"
    assert row["headline"] == "Tesla expands production"


def test_screener_put_call_ratio(patch_resolvers):
    patch_resolvers(mod)
    req = mod.ScreenerOptionalMarketReq(market="S&P 500")
    out = mod.screener_put_call_ratio(req)
    assert out["count"] == 1
    row = out["rows"][0]
    assert row["ticker"] == "AAPL"
    assert row["put_call_ratio"] == 0.65
    assert row["call_count"] == 500000
    assert row["put_count"] == 325000


def test_screener_linkedin(patch_resolvers):
    patch_resolvers(mod)
    req = mod.ScreenerMarketReq(market="S&P 500")
    out = mod.screener_linkedin(req)
    assert out["count"] == 1
    row = out["rows"][0]
    assert row["ticker"] == "AMZN"
    assert row["employee_count"] == 1500000
    assert row["followers_count"] == 35000000
    assert row["job_count"] == 12000


def test_screener_app_ratings(patch_resolvers):
    patch_resolvers(mod)
    req = mod.ScreenerMarketReq(market="S&P 500")
    out = mod.screener_app_ratings(req)
    assert out["count"] == 1
    row = out["rows"][0]
    assert row["ticker"] == "AMZN"
    assert row["app_store_score"] == 4.7
    assert row["play_store_score"] == 4.3


def test_screener_csv_format(patch_resolvers):
    patch_resolvers(mod)
    req = mod.ScreenerMarketReq(market="S&P 500", format="csv")
    out = mod.screener_sentiment(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    assert "ticker" in header
    assert "score" in header
