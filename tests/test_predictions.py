from finbrain_mcp.tools import predictions as mod


def test_predictions_market(patch_resolvers):
    patch_resolvers(mod)
    req = mod.PredictionsMarketReq(market="S&P 500", limit=1)
    out = mod.predictions_by_market(req)
    assert out["count"] == 1
    row = out["rows"][0]
    # flattened normalized keys (no nested "prediction")
    for key in [
        "ticker",
        "expected_short",
        "expected_mid",
        "expected_long",
        "last_update",
        "type",
    ]:
        assert key in row


def test_predictions_ticker_daily(patch_resolvers):
    patch_resolvers(mod)
    out = mod.predictions_by_ticker(mod.PredictionsTickerReq(ticker="AMZN"))
    assert out["format"] == "json"
    assert out["ticker"] == "AMZN"
    assert out["type"] == "daily"
    assert out["series_total"] >= 1
    assert {"date", "mid", "low", "high"} <= set(out["series"][0].keys())


def test_predictions_ticker_monthly(patch_resolvers):
    patch_resolvers(mod)
    out = mod.predictions_by_ticker(
        mod.PredictionsTickerReq(ticker="AMZN", prediction_type="monthly")
    )
    assert out["type"] == "monthly"
    assert out["series_total"] >= 1
