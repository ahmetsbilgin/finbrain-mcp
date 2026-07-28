from finbrain_mcp.tools import senate_trades as mod


def test_senate_trades_normalized_json(patch_resolvers):
    patch_resolvers(mod)
    req = mod.SenateTradesReq(ticker="META", limit=2)
    out = mod.senate_trades_by_ticker(req)
    assert out["format"] == "json"
    assert out["ticker"] == "META"
    assert out["series_total"] == 2
    rows = out["series"]
    # dates are ascending: first is 2025-10-31, then 2025-11-13
    assert rows[0]["date"] == "2025-10-31"
    assert rows[0]["senator"] == "John Boozman"
    assert rows[0]["trade_type"] == "Purchase"
    assert rows[0]["amount_min"] == 1001.0
    assert rows[0]["amount_max"] == 15000.0
    assert rows[0]["amount_exact"] is False
    assert rows[0]["amount_raw"].startswith("$1,001")
    # Historical row a reconcile could not fill.
    assert rows[0]["disclosure_date"] is None
    # Blank owner column on a Senate filing reports as UNKNOWN.
    assert rows[0]["owner"] == "UNKNOWN"
    assert rows[0]["amount_as_filed"] is None
    assert rows[0]["amount_flag"] is None

    assert rows[1]["date"] == "2025-11-13"
    assert rows[1]["senator"] == "Shelley Moore Capito"
    assert rows[1]["trade_type"] == "Purchase"
    assert rows[1]["amount_min"] == 1001.0
    assert rows[1]["amount_max"] == 15000.0
    assert rows[1]["amount_exact"] is False
    assert rows[1]["disclosure_date"] == "2025-12-04"
    assert rows[1]["owner"] == "SP"
    assert rows[1]["amount_as_filed"] is None
    assert rows[1]["amount_flag"] is None


def test_senate_trades_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.SenateTradesReq(ticker="META", format="csv", limit=2)
    out = mod.senate_trades_by_ticker(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    for col in [
        "date",
        "senator",
        "trade_type",
        "amount_min",
        "amount_max",
        "amount_exact",
        "amount_raw",
        "disclosure_date",
        "owner",
        "amount_as_filed",
        "amount_flag",
    ]:
        assert col in header
