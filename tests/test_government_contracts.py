import finbrain_mcp.tools.government_contracts as ticker_mod
import finbrain_mcp.tools.screener as screener_mod


# ---------- per-ticker tool ----------

def test_government_contracts_normalized_json(patch_resolvers):
    patch_resolvers(ticker_mod)
    req = ticker_mod.GovernmentContractsReq(ticker="LMT", limit=10)
    out = ticker_mod.government_contracts_by_ticker(req)

    assert out["format"] == "json"
    assert out["ticker"] == "LMT"
    assert out["name"] == "Lockheed Martin Corporation"
    assert out["series_total"] == 2
    assert out["series_count"] == 2

    rows = out["series"]
    # sorted by start_date ascending: 2025-03-15, then 2025-06-01
    assert rows[0]["start_date"] == "2025-03-15"
    assert rows[0]["award_id"] == "CONT_AWD_0002"
    assert rows[0]["award_amount"] == 12000000.0
    assert rows[0]["award_type"] == ""
    assert rows[0]["awarding_agency"] == "NASA"
    assert rows[0]["awarding_sub_agency"] == "NASA Headquarters"
    assert rows[0]["recipient_name"] == "Lockheed Martin Corporation"
    assert rows[0]["end_date"] == "2027-03-15"
    assert rows[0]["description"] == "Space systems development"
    assert rows[0]["naics_code"] == "336414"
    assert rows[0]["naics_description"] == "Guided Missile and Space Vehicle Manufacturing"
    assert rows[0]["contract_award_type"] == ""

    assert rows[1]["start_date"] == "2025-06-01"
    assert rows[1]["award_id"] == "CONT_AWD_0001"
    assert rows[1]["award_amount"] == 50000000.0
    assert rows[1]["awarding_agency"] == "Department of Defense"
    assert rows[1]["awarding_sub_agency"] == "Department of the Army"
    assert rows[1]["end_date"] == "2026-06-01"
    assert rows[1]["description"] == "Aircraft maintenance services"
    assert rows[1]["naics_code"] == "336411"
    assert rows[1]["naics_description"] == "Aircraft Manufacturing"


def test_government_contracts_csv(patch_resolvers):
    patch_resolvers(ticker_mod)
    req = ticker_mod.GovernmentContractsReq(ticker="LMT", format="csv", limit=10)
    out = ticker_mod.government_contracts_by_ticker(req)

    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    for col in [
        "award_id",
        "award_amount",
        "awarding_agency",
        "awarding_sub_agency",
        "recipient_name",
        "start_date",
        "end_date",
        "description",
        "naics_code",
        "naics_description",
    ]:
        assert col in header


def test_government_contracts_limit(patch_resolvers):
    patch_resolvers(ticker_mod)
    req = ticker_mod.GovernmentContractsReq(ticker="LMT", limit=1)
    out = ticker_mod.government_contracts_by_ticker(req)

    assert out["series_count"] == 1
    assert out["series_total"] == 2
    # limit returns the latest entry (last after sort)
    assert out["series"][0]["start_date"] == "2025-06-01"


# ---------- screener tool ----------

def test_screener_government_contracts_json(patch_resolvers):
    patch_resolvers(screener_mod)
    req = screener_mod.ScreenerLimitOnlyReq(limit=100)
    out = screener_mod.screener_government_contracts(req)

    assert out["format"] == "json"
    assert out["count"] == 2

    rows = out["rows"]
    assert rows[0]["ticker"] == "LMT"
    assert rows[0]["award_amount"] == 50000000.0
    assert rows[0]["awarding_agency"] == "Department of Defense"
    assert rows[0]["naics_description"] == "Aircraft Manufacturing"
    assert rows[1]["ticker"] == "BA"

    # summary should have snake_case keys
    summary = out["summary"]
    assert summary["total_contracts"] == 2
    assert summary["total_tickers"] == 2
    assert summary["total_value"] == 130000000.0


def test_screener_government_contracts_csv(patch_resolvers):
    patch_resolvers(screener_mod)
    req = screener_mod.ScreenerLimitOnlyReq(format="csv")
    out = screener_mod.screener_government_contracts(req)

    assert out["format"] == "csv"
    lines = out["data"].strip().split("\n")
    header = lines[0]
    assert "ticker" in header
    assert "award_amount" in header
    # CSV should not include summary
    assert "summary" not in out
