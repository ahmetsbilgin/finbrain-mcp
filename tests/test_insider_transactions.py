from finbrain_mcp.tools import insider_transactions as mod


def test_insider_transactions_normalized_json(patch_resolvers):
    patch_resolvers(mod)
    req = mod.InsiderReq(market="S&P 500", ticker="AMZN", limit=2)
    out = mod.insider_transactions_by_ticker(req)
    assert out["format"] == "json"
    assert out["ticker"] == "AMZN"
    assert out["series_total"] == 2

    row0 = out["series"][0]
    # Keys present
    for k in [
        "date",
        "date_raw",
        "insider_name",
        "relationship",
        "transaction_type",
        "price",
        "shares",
        "usd_value",
        "total_shares",
        "sec_form4_date",
        "sec_form4_datetime",
        "sec_form4_link",
    ]:
        assert k in row0

    # Date parsing
    assert row0["date"] in ("2024-02-10", "2024-03-08")  # ascending order
    # Types
    assert isinstance(row0["shares"], int) or row0["shares"] is None
    assert isinstance(row0["price"], float) or row0["price"] is None


def test_insider_transactions_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.InsiderReq(market="S&P 500", ticker="AMZN", format="csv", limit=1)
    out = mod.insider_transactions_by_ticker(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    for col in [
        "date",
        "insider_name",
        "transaction_type",
        "usd_value",
        "sec_form4_link",
    ]:
        assert col in header
