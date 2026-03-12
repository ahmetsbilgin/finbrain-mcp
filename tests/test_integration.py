"""
Integration tests that hit the real FinBrain v2 API.

Skipped automatically when FINBRAIN_API_KEY is not set.
Run with:  FINBRAIN_API_KEY=your_key pytest tests/test_integration.py -v
"""

from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("FINBRAIN_API_KEY"),
    reason="FINBRAIN_API_KEY not set",
)

TICKER = "AAPL"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _client():
    from finbrain_mcp.client_adapter import FBClient
    from finbrain_mcp.auth import resolve_api_key

    return FBClient(resolve_api_key())


def _assert_series_shape(obj: dict, min_keys: set[str]):
    """Common assertions for endpoints that return {ticker, name, series}."""
    assert isinstance(obj, dict)
    assert obj.get("ticker") is not None
    assert isinstance(obj.get("series"), list)
    if obj["series"]:
        assert min_keys <= set(obj["series"][0].keys())


# ---------------------------------------------------------------------------
# availability
# ---------------------------------------------------------------------------

class TestAvailability:
    def test_markets(self):
        markets = _client().available_markets()
        assert isinstance(markets, list)
        assert len(markets) > 0
        assert all(isinstance(m, str) for m in markets)

    def test_tickers(self):
        tickers = _client().available_tickers("daily")
        assert isinstance(tickers, list)
        assert len(tickers) > 0
        assert "symbol" in tickers[0] or "ticker" in tickers[0]


# ---------------------------------------------------------------------------
# predictions
# ---------------------------------------------------------------------------

class TestPredictions:
    def test_ticker_daily(self):
        obj = _client().predictions_ticker(TICKER, prediction_type="daily")
        assert obj["ticker"] == TICKER
        assert obj["type"] == "daily"
        assert len(obj["series"]) > 0
        row = obj["series"][0]
        assert {"date", "mid", "low", "high"} <= set(row.keys())
        assert isinstance(row["mid"], float)

    def test_ticker_monthly(self):
        obj = _client().predictions_ticker(TICKER, prediction_type="monthly")
        assert obj["type"] == "monthly"
        assert len(obj["series"]) > 0

    def test_screener_daily(self):
        rows = _client().screener_predictions(
            prediction_type="daily", market="S&P 500", limit=5
        )
        assert isinstance(rows, list)
        assert len(rows) > 0
        assert "ticker" in rows[0]
        assert "expected_short" in rows[0]


# ---------------------------------------------------------------------------
# sentiments
# ---------------------------------------------------------------------------

class TestSentiments:
    def test_ticker(self):
        obj = _client().sentiments_ticker(TICKER, None, None)
        _assert_series_shape(obj, {"date", "score"})
        assert isinstance(obj["series"][0]["score"], float)


# ---------------------------------------------------------------------------
# analyst ratings
# ---------------------------------------------------------------------------

class TestAnalystRatings:
    def test_ticker(self):
        obj = _client().analyst_ratings_ticker(TICKER, None, None)
        _assert_series_shape(obj, {"date", "institution", "rating_type", "signal"})


# ---------------------------------------------------------------------------
# app ratings
# ---------------------------------------------------------------------------

class TestAppRatings:
    def test_ticker(self):
        obj = _client().app_ratings_ticker(TICKER, None, None)
        _assert_series_shape(obj, {"date", "play_store_score", "app_store_score"})


# ---------------------------------------------------------------------------
# house trades
# ---------------------------------------------------------------------------

class TestHouseTrades:
    def test_ticker(self):
        obj = _client().house_trades_ticker(TICKER, None, None)
        _assert_series_shape(obj, {"date", "representative", "trade_type", "amount_raw"})


# ---------------------------------------------------------------------------
# senate trades
# ---------------------------------------------------------------------------

class TestSenateTrades:
    def test_ticker(self):
        obj = _client().senate_trades_ticker(TICKER, None, None)
        _assert_series_shape(obj, {"date", "senator", "trade_type", "amount_raw"})


# ---------------------------------------------------------------------------
# corporate lobbying
# ---------------------------------------------------------------------------

class TestCorporateLobbying:
    def test_ticker(self):
        obj = _client().corporate_lobbying_ticker(TICKER, None, None)
        _assert_series_shape(obj, {"date", "filing_uuid", "filing_year", "quarter",
                                   "client_name", "registrant_name", "income", "expenses"})


# ---------------------------------------------------------------------------
# insider transactions
# ---------------------------------------------------------------------------

class TestInsiderTransactions:
    def test_ticker(self):
        obj = _client().insider_transactions_ticker(TICKER)
        _assert_series_shape(obj, {"date", "insider_name", "transaction_type", "shares"})


# ---------------------------------------------------------------------------
# linkedin
# ---------------------------------------------------------------------------

class TestLinkedIn:
    def test_ticker(self):
        obj = _client().linkedin_ticker(TICKER, None, None)
        _assert_series_shape(obj, {"date", "employee_count", "followers_count"})


# ---------------------------------------------------------------------------
# options
# ---------------------------------------------------------------------------

class TestOptions:
    def test_put_call(self):
        obj = _client().options_put_call(TICKER, None, None)
        _assert_series_shape(obj, {"date", "put_call_ratio", "call_count", "put_count"})


# ---------------------------------------------------------------------------
# tool-level round-trip (calls tool functions directly)
# ---------------------------------------------------------------------------

class TestToolRoundTrip:
    """Call actual tool functions end-to-end (no mocking)."""

    def test_predictions_by_ticker(self):
        from finbrain_mcp.tools.predictions import predictions_by_ticker, PredictionsTickerReq

        out = predictions_by_ticker(PredictionsTickerReq(ticker=TICKER))
        assert out["format"] == "json"
        assert out["ticker"] == TICKER
        assert out["series_total"] > 0

    def test_news_sentiment(self):
        from finbrain_mcp.tools.sentiments import news_sentiment_by_ticker, SentimentsReq

        out = news_sentiment_by_ticker(SentimentsReq(ticker=TICKER, limit=5))
        assert out["format"] == "json"
        assert out["series_count"] <= 5

    def test_options_csv(self):
        from finbrain_mcp.tools.options import options_put_call, PutCallReq

        out = options_put_call(PutCallReq(ticker=TICKER, format="csv", limit=3))
        assert out["format"] == "csv"
        lines = out["data"].strip().splitlines()
        assert len(lines) >= 2  # header + at least 1 row
        assert "put_call_ratio" in lines[0]

    def test_corporate_lobbying(self):
        from finbrain_mcp.tools.corporate_lobbying import (
            corporate_lobbying_by_ticker,
            CorporateLobbyingReq,
        )

        out = corporate_lobbying_by_ticker(CorporateLobbyingReq(ticker=TICKER, limit=5))
        assert out["format"] == "json"
        assert out["ticker"] == TICKER
        assert out["series_count"] <= 5
