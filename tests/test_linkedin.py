from finbrain_mcp.tools import linkedin as mod


def test_linkedin_metrics_json_series(patch_resolvers):
    patch_resolvers(mod)
    req = mod.LinkedInReq(market="S&P 500", ticker="AMZN", limit=1)
    out = mod.linkedin_metrics_by_ticker(req)
    assert out["format"] == "json"
    assert out["ticker"] == "AMZN"
    assert out["series_count"] == 1
    assert out["series_total"] == 2

    row = out["series"][0]
    assert set(["date", "employee_count", "followers_count"]).issubset(row.keys())
    assert isinstance(row["employee_count"], int) or row["employee_count"] is None
    assert isinstance(row["followers_count"], int) or row["followers_count"] is None


def test_linkedin_metrics_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.LinkedInReq(market="S&P 500", ticker="AMZN", format="csv", limit=2)
    out = mod.linkedin_metrics_by_ticker(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    assert "employee_count" in header and "followers_count" in header
