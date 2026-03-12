from finbrain_mcp.tools import corporate_lobbying as mod


def test_corporate_lobbying_normalized_json(patch_resolvers):
    patch_resolvers(mod)
    req = mod.CorporateLobbyingReq(ticker="AAPL", limit=10)
    out = mod.corporate_lobbying_by_ticker(req)
    assert out["format"] == "json"
    assert out["ticker"] == "AAPL"
    assert out["name"] == "Apple Inc."
    assert out["series_total"] == 2
    assert out["series_count"] == 2
    rows = out["series"]
    # dates are ascending after normalization: 2023-10-20, then 2024-01-15
    assert rows[0]["date"] == "2023-10-20"
    assert rows[0]["filing_uuid"] == "uuid-002"
    assert rows[0]["filing_year"] == 2023
    assert rows[0]["quarter"] == "Q4"
    assert rows[0]["client_name"] == "Apple Inc."
    assert rows[0]["registrant_name"] == "Franklin Square Group"
    assert rows[0]["income"] == 200000.0
    assert rows[0]["expenses"] == 180000.0
    assert rows[0]["issue_codes"] == ["CPT", "IMM"]
    assert rows[0]["government_entities"] == ["U.S. Senate"]

    assert rows[1]["date"] == "2024-01-15"
    assert rows[1]["filing_uuid"] == "uuid-001"
    assert rows[1]["filing_year"] == 2024
    assert rows[1]["quarter"] == "Q1"
    assert rows[1]["registrant_name"] == "Fierce Government Relations"
    assert rows[1]["income"] == 150000.0
    assert rows[1]["expenses"] == 120000.0
    assert rows[1]["issue_codes"] == ["TAX", "TEC"]
    assert rows[1]["government_entities"] == ["U.S. Senate", "U.S. House of Representatives"]


def test_corporate_lobbying_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.CorporateLobbyingReq(ticker="AAPL", format="csv", limit=10)
    out = mod.corporate_lobbying_by_ticker(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    for col in [
        "date",
        "filing_uuid",
        "filing_year",
        "quarter",
        "client_name",
        "registrant_name",
        "income",
        "expenses",
    ]:
        assert col in header


def test_corporate_lobbying_limit(patch_resolvers):
    patch_resolvers(mod)
    req = mod.CorporateLobbyingReq(ticker="AAPL", limit=1)
    out = mod.corporate_lobbying_by_ticker(req)
    assert out["series_count"] == 1
    assert out["series_total"] == 2
    # limit returns the latest entry (last after sort)
    assert out["series"][0]["date"] == "2024-01-15"
