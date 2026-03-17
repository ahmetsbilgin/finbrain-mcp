import finbrain_mcp.tools.reddit_mentions as ticker_mod
import finbrain_mcp.tools.screener as screener_mod


# ---------- per-ticker tool ----------

def test_reddit_mentions_normalized_json(patch_resolvers):
    patch_resolvers(ticker_mod)
    req = ticker_mod.RedditMentionsReq(ticker="TSLA", limit=100)
    out = ticker_mod.reddit_mentions_by_ticker(req)

    assert out["format"] == "json"
    assert out["ticker"] == "TSLA"
    assert out["name"] == "Tesla, Inc."
    assert out["series_total"] == 4
    assert out["series_count"] == 4

    # series should be sorted by date
    rows = out["series"]
    dates = [r["date"] for r in rows]
    assert dates == sorted(dates)

    # check field names and types
    row = rows[0]
    assert "date" in row
    assert "subreddit" in row
    assert "mentions" in row
    assert isinstance(row["mentions"], int)


def test_reddit_mentions_csv(patch_resolvers):
    patch_resolvers(ticker_mod)
    req = ticker_mod.RedditMentionsReq(ticker="TSLA", format="csv")
    out = ticker_mod.reddit_mentions_by_ticker(req)

    assert out["format"] == "csv"
    lines = out["data"].strip().split("\n")
    header = lines[0]
    assert "date" in header
    assert "subreddit" in header
    assert "mentions" in header
    assert len(lines) == 5  # header + 4 data rows


def test_reddit_mentions_limit(patch_resolvers):
    patch_resolvers(ticker_mod)
    req = ticker_mod.RedditMentionsReq(ticker="TSLA", limit=2)
    out = ticker_mod.reddit_mentions_by_ticker(req)

    assert out["series_count"] == 2
    assert out["series_total"] == 4


# ---------- screener tool ----------

def test_screener_reddit_mentions_json(patch_resolvers):
    patch_resolvers(screener_mod)
    req = screener_mod.ScreenerOptionalMarketReq(limit=100)
    out = screener_mod.screener_reddit_mentions(req)

    assert out["format"] == "json"
    assert out["count"] == 2

    rows = out["rows"]
    assert rows[0]["ticker"] == "TSLA"
    assert rows[0]["total_mentions"] == 120
    assert rows[0]["subreddits"] == {"wallstreetbets": 85, "stocks": 12}
    assert rows[1]["ticker"] == "AAPL"

    # summary should have snake_case keys
    summary = out["summary"]
    assert summary["total_entries"] == 2
    assert summary["total_tickers"] == 2
    assert summary["average_mentions"] == 82.5
    assert summary["top_mentioned"] == ["TSLA", "AAPL"]
    assert "wallstreetbets" in summary["subreddit_names"]


def test_screener_reddit_mentions_csv(patch_resolvers):
    patch_resolvers(screener_mod)
    req = screener_mod.ScreenerOptionalMarketReq(format="csv")
    out = screener_mod.screener_reddit_mentions(req)

    assert out["format"] == "csv"
    lines = out["data"].strip().split("\n")
    header = lines[0]
    assert "ticker" in header
    assert "total_mentions" in header
    # CSV should not include summary
    assert "summary" not in out
