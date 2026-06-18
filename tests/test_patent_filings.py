import finbrain_mcp.tools.patent_filings as ticker_mod
import finbrain_mcp.tools.screener as screener_mod


# ---------- per-ticker tool ----------

def test_patent_filings_normalized_json(patch_resolvers):
    patch_resolvers(ticker_mod)
    req = ticker_mod.PatentFilingsReq(ticker="AAPL", limit=10)
    out = ticker_mod.patent_filings_by_ticker(req)

    assert out["format"] == "json"
    assert out["ticker"] == "AAPL"
    assert out["name"] == "Apple Inc."
    assert out["series_total"] == 2
    assert out["series_count"] == 2

    rows = out["series"]
    # sorted by patent_date ascending: 2025-03-15, then 2025-06-01
    assert rows[0]["patent_date"] == "2025-03-15"
    assert rows[0]["patent_id"] == "12345679"
    assert rows[0]["title"] == "Display panel with adaptive refresh"
    assert rows[0]["type"] == "utility"
    assert rows[0]["kind"] == "B2"
    assert rows[0]["num_claims"] == 15
    assert rows[0]["num_cited_by"] == 2
    assert rows[0]["assignee_organization"] == "Apple Inc."
    assert rows[0]["assignee_type"] == "2"
    assert rows[0]["application_filing_date"] == "2021-11-01"
    assert rows[0]["filing_to_grant_days"] == 865
    assert rows[0]["inventors"] == ["Alice Smith"]
    assert rows[0]["num_inventors"] == 1
    assert rows[0]["cpc_sections"] == ["G"]
    assert rows[0]["cpc_subsections"] == ["G09"]
    assert rows[0]["primary_cpc_section"] == "G"

    assert rows[1]["patent_date"] == "2025-06-01"
    assert rows[1]["patent_id"] == "12345678"
    assert rows[1]["num_claims"] == 20
    assert rows[1]["inventors"] == ["Jane Doe", "John Roe"]
    assert rows[1]["cpc_sections"] == ["G", "H"]


def test_patent_filings_csv(patch_resolvers):
    patch_resolvers(ticker_mod)
    req = ticker_mod.PatentFilingsReq(ticker="AAPL", format="csv", limit=10)
    out = ticker_mod.patent_filings_by_ticker(req)

    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    for col in [
        "patent_id",
        "patent_date",
        "title",
        "type",
        "kind",
        "num_claims",
        "num_cited_by",
        "assignee_organization",
        "application_filing_date",
        "primary_cpc_section",
    ]:
        assert col in header


def test_patent_filings_limit(patch_resolvers):
    patch_resolvers(ticker_mod)
    req = ticker_mod.PatentFilingsReq(ticker="AAPL", limit=1)
    out = ticker_mod.patent_filings_by_ticker(req)

    assert out["series_count"] == 1
    assert out["series_total"] == 2
    # limit returns the latest entry (last after sort)
    assert out["series"][0]["patent_date"] == "2025-06-01"


# ---------- screener tool ----------

def test_screener_patent_filings_json(patch_resolvers):
    patch_resolvers(screener_mod)
    req = screener_mod.ScreenerLimitOnlyReq(limit=100)
    out = screener_mod.screener_patent_filings(req)

    assert out["format"] == "json"
    assert out["count"] == 2

    rows = out["rows"]
    assert rows[0]["ticker"] == "AAPL"
    assert rows[0]["patent_id"] == "12345678"
    assert rows[0]["title"] == "On-device machine learning"
    assert rows[0]["num_claims"] == 20
    assert rows[0]["primary_cpc_section"] == "G"
    assert rows[1]["ticker"] == "MSFT"

    # summary should have snake_case keys
    summary = out["summary"]
    assert summary["total_patents"] == 2
    assert summary["total_tickers"] == 2
    assert summary["top_cpc_sections"] == ["G"]


def test_screener_patent_filings_csv(patch_resolvers):
    patch_resolvers(screener_mod)
    req = screener_mod.ScreenerLimitOnlyReq(format="csv")
    out = screener_mod.screener_patent_filings(req)

    assert out["format"] == "csv"
    lines = out["data"].strip().split("\n")
    header = lines[0]
    assert "ticker" in header
    assert "patent_id" in header
    assert "num_claims" in header
    # CSV should not include summary
    assert "summary" not in out
