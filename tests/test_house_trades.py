from finbrain_mcp.tools import house_trades as mod


def test_house_trades_normalized_json(patch_resolvers):
    patch_resolvers(mod)
    req = mod.HouseTradesReq(market="S&P 500", ticker="AMZN", limit=2)
    out = mod.house_trades_by_ticker(req)
    assert out["format"] == "json"
    assert out["ticker"] == "AMZN"
    assert out["series_total"] == 2
    rows = out["series"]
    # dates are ascending: first is 2024-01-25 (range), then 2024-02-29 (exact)
    assert rows[0]["date"] == "2024-01-25"
    assert rows[0]["representative"] == "Shri Thanedar"
    assert rows[0]["trade_type"] == "Sale"
    assert rows[0]["amount_min"] == 15001.0
    assert rows[0]["amount_max"] == 50000.0
    assert rows[0]["amount_exact"] is False
    assert rows[0]["amount_raw"].startswith("$15,001")

    assert rows[1]["date"] == "2024-02-29"
    assert rows[1]["representative"] == "Pete Sessions"
    assert rows[1]["trade_type"] == "Purchase"
    assert rows[1]["amount_min"] == 360.0
    assert rows[1]["amount_max"] == 360.0
    assert rows[1]["amount_exact"] is True


def test_house_trades_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.HouseTradesReq(market="S&P 500", ticker="AMZN", format="csv", limit=2)
    out = mod.house_trades_by_ticker(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    for col in [
        "date",
        "representative",
        "trade_type",
        "amount_min",
        "amount_max",
        "amount_exact",
        "amount_raw",
    ]:
        assert col in header
