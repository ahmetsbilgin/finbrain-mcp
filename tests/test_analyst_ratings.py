from finbrain_mcp.tools import analyst_ratings as mod


def test_analyst_ratings_json_series(patch_resolvers):
    patch_resolvers(mod)
    req = mod.AnalystRatingsReq(market="S&P 500", ticker="AMZN", limit=1)
    out = mod.analyst_ratings_by_ticker(req)
    assert out["format"] == "json"
    assert out["ticker"] == "AMZN"
    assert out["series_count"] == 1
    assert out["series_total"] == 2

    row = out["series"][0]
    for k in [
        "date",
        "rating_type",
        "institution",
        "signal",
        "target_price_from",
        "target_price_to",
        "target_price_raw",
    ]:
        assert k in row

    # parsed floats look sane
    assert (
        isinstance(row["target_price_from"], float) or row["target_price_from"] is None
    )


def test_analyst_ratings_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.AnalystRatingsReq(market="S&P 500", ticker="AMZN", format="csv", limit=2)
    out = mod.analyst_ratings_by_ticker(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    assert "rating_type" in header
    assert "target_price_from" in header
