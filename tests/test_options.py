from finbrain_mcp.tools import options as mod


def test_options_put_call_json_series(patch_resolvers):
    patch_resolvers(mod)
    req = mod.PutCallReq(market="S&P 500", ticker="AMZN", limit=1)
    out = mod.options_put_call(req)
    assert out["format"] == "json"
    assert out["ticker"] == "AMZN"
    assert out["series_total"] == 2
    assert out["series_count"] == 1

    row = out["series"][0]
    assert set(["date", "put_call_ratio", "call_count", "put_count"]).issubset(
        row.keys()
    )
    assert isinstance(row["put_call_ratio"], float) or row["put_call_ratio"] is None
    assert isinstance(row["call_count"], int) or row["call_count"] is None
    assert isinstance(row["put_count"], int) or row["put_count"] is None


def test_options_put_call_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.PutCallReq(market="S&P 500", ticker="AMZN", format="csv", limit=2)
    out = mod.options_put_call(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    for col in ["date", "put_call_ratio", "call_count", "put_count"]:
        assert col in header
