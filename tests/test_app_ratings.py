from finbrain_mcp.tools import app_ratings as mod


def test_app_ratings_json_series(patch_resolvers):
    patch_resolvers(mod)
    req = mod.AppRatingsReq(market="S&P 500", ticker="AMZN", limit=1)
    out = mod.app_ratings_by_ticker(req)
    assert out["format"] == "json"
    assert out["ticker"] == "AMZN"
    assert out["series_count"] == 1
    assert out["series_total"] == 2

    row = out["series"][0]
    # snake_case keys exist
    for k in [
        "date",
        "play_store_score",
        "play_store_ratings_count",
        "app_store_score",
        "app_store_ratings_count",
        "play_store_install_count",
    ]:
        assert k in row

    # types look right
    assert isinstance(row["play_store_score"], float) or row["play_store_score"] is None
    assert (
        isinstance(row["play_store_ratings_count"], int)
        or row["play_store_ratings_count"] is None
    )


def test_app_ratings_csv(patch_resolvers):
    patch_resolvers(mod)
    req = mod.AppRatingsReq(market="S&P 500", ticker="AMZN", format="csv", limit=2)
    out = mod.app_ratings_by_ticker(req)
    assert out["format"] == "csv"
    header = out["data"].splitlines()[0]
    assert "play_store_score" in header
    assert "app_store_ratings_count" in header
