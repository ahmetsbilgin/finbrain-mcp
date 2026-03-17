from __future__ import annotations
from typing import Any, List, Literal
from .utils import df_to_records_maybe
from .normalizers import (
    normalize_available_markets,
    normalize_screener_predictions,
    normalize_ticker_predictions,
    normalize_sentiments_ticker,
    normalize_app_ratings_ticker,
    normalize_analyst_ratings_ticker,
    normalize_house_trades_ticker,
    normalize_senate_trades_ticker,
    normalize_corporate_lobbying_ticker,
    normalize_insider_transactions_ticker,
    normalize_linkedin_ticker,
    normalize_options_put_call_ticker,
    normalize_news_ticker,
    normalize_screener_sentiment,
    normalize_screener_analyst_ratings,
    normalize_screener_insider_trading,
    normalize_screener_congress,
    normalize_screener_news,
    normalize_screener_put_call,
    normalize_screener_linkedin,
    normalize_screener_app_ratings,
    normalize_reddit_mentions_ticker,
    normalize_screener_reddit_mentions,
    normalize_screener_reddit_mentions_summary,
)

# SDK import (PyPI package name is finbrain-python; import path is `finbrain`)
from finbrain import FinBrainClient  # type: ignore[import-untyped]


class FBClient:
    """
    Thin wrapper around finbrain-python SDK (v0.2.0+, targeting API v2).
    Always requests JSON (not DataFrame). Falls back to DF->records if SDK
    returns a DataFrame for any reason.
    """

    def __init__(self, api_key: str):
        self.fb = FinBrainClient(api_key=api_key)

    # ---------- availability ----------
    def available_markets(self) -> List[str] | Any:
        raw = self.fb.available.markets()
        return normalize_available_markets(raw)

    def available_tickers(self, dataset: Literal["daily", "monthly"]) -> Any:
        out = self.fb.available.tickers(dataset, as_dataframe=False)
        return df_to_records_maybe(out)

    def available_regions(self) -> Any:
        return self.fb.available.regions(as_dataframe=False)

    # ---------- app ratings ----------
    def app_ratings_ticker(
        self, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.app_ratings.ticker(
            ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_app_ratings_ticker(raw)

    # ---------- analyst ratings ----------
    def analyst_ratings_ticker(
        self, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.analyst_ratings.ticker(
            ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_analyst_ratings_ticker(raw)

    # ---------- house trades ----------
    def house_trades_ticker(
        self, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.house_trades.ticker(
            ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_house_trades_ticker(raw)

    # ---------- senate trades ----------
    def senate_trades_ticker(
        self, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.senate_trades.ticker(
            ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_senate_trades_ticker(raw)

    # ---------- corporate lobbying ----------
    def corporate_lobbying_ticker(
        self, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.corporate_lobbying.ticker(
            ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_corporate_lobbying_ticker(raw)

    # ---------- insider transactions ----------
    def insider_transactions_ticker(
        self, ticker: str, date_from: str | None = None, date_to: str | None = None
    ) -> Any:
        raw = self.fb.insider_transactions.ticker(
            ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_insider_transactions_ticker(raw)

    # ---------- LinkedIn metrics ----------
    def linkedin_ticker(
        self, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.linkedin_data.ticker(
            ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_linkedin_ticker(raw)

    # ---------- options put/call ----------
    def options_put_call(
        self, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.options.put_call(
            ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_options_put_call_ticker(raw)

    # ---------- price predictions ----------
    def screener_predictions(
        self,
        prediction_type: Literal["daily", "monthly"],
        market: str | None = None,
        region: str | None = None,
        limit: int | None = None,
    ) -> Any:
        method = (
            self.fb.screener.predictions_daily
            if prediction_type == "daily"
            else self.fb.screener.predictions_monthly
        )
        raw = method(market=market, region=region, limit=limit, as_dataframe=False)
        items = df_to_records_maybe(raw)
        return normalize_screener_predictions(items)

    def predictions_ticker(
        self, ticker: str, prediction_type: Literal["daily", "monthly"]
    ) -> Any:
        raw = self.fb.predictions.ticker(
            ticker, prediction_type=prediction_type, as_dataframe=False
        )
        return normalize_ticker_predictions(raw)

    # ---------- news sentiment ----------
    def sentiments_ticker(
        self, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.sentiments.ticker(
            ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_sentiments_ticker(raw)

    # ---------- news articles ----------
    def news_ticker(
        self,
        ticker: str,
        date_from: str | None = None,
        date_to: str | None = None,
        limit: int | None = None,
    ) -> Any:
        raw = self.fb.news.ticker(
            ticker, date_from=date_from, date_to=date_to, limit=limit, as_dataframe=False
        )
        return normalize_news_ticker(raw)

    # ---------- recent endpoints ----------
    def recent_news(
        self,
        limit: int | None = None,
        market: str | None = None,
        region: str | None = None,
    ) -> Any:
        raw = self.fb.recent.news(limit=limit, market=market, region=region, as_dataframe=False)
        items = df_to_records_maybe(raw)
        return normalize_screener_news(items)

    def recent_analyst_ratings(
        self,
        limit: int | None = None,
        market: str | None = None,
        region: str | None = None,
    ) -> Any:
        raw = self.fb.recent.analyst_ratings(
            limit=limit, market=market, region=region, as_dataframe=False
        )
        items = df_to_records_maybe(raw)
        return normalize_screener_analyst_ratings(items)

    # ---------- screener endpoints ----------
    def screener_sentiment(
        self,
        market: str | None = None,
        region: str | None = None,
        limit: int | None = None,
    ) -> Any:
        raw = self.fb.screener.sentiment(
            market=market, region=region, limit=limit, as_dataframe=False
        )
        items = df_to_records_maybe(raw)
        return normalize_screener_sentiment(items)

    def screener_analyst_ratings(
        self,
        market: str | None = None,
        region: str | None = None,
        limit: int | None = None,
    ) -> Any:
        raw = self.fb.screener.analyst_ratings(
            market=market, region=region, limit=limit, as_dataframe=False
        )
        items = df_to_records_maybe(raw)
        return normalize_screener_analyst_ratings(items)

    def screener_insider_trading(
        self, limit: int | None = None
    ) -> Any:
        raw = self.fb.screener.insider_trading(limit=limit, as_dataframe=False)
        items = df_to_records_maybe(raw)
        return normalize_screener_insider_trading(items)

    def screener_congress_house(
        self, limit: int | None = None
    ) -> Any:
        raw = self.fb.screener.congress_house(limit=limit, as_dataframe=False)
        items = df_to_records_maybe(raw)
        return normalize_screener_congress(items)

    def screener_congress_senate(
        self, limit: int | None = None
    ) -> Any:
        raw = self.fb.screener.congress_senate(limit=limit, as_dataframe=False)
        items = df_to_records_maybe(raw)
        return normalize_screener_congress(items)

    def screener_news(
        self,
        market: str | None = None,
        region: str | None = None,
        limit: int | None = None,
    ) -> Any:
        raw = self.fb.screener.news(
            market=market, region=region, limit=limit, as_dataframe=False
        )
        items = df_to_records_maybe(raw)
        return normalize_screener_news(items)

    def screener_put_call_ratio(
        self,
        market: str | None = None,
        region: str | None = None,
        limit: int | None = None,
    ) -> Any:
        raw = self.fb.screener.put_call_ratio(
            market=market, region=region, limit=limit, as_dataframe=False
        )
        items = df_to_records_maybe(raw)
        return normalize_screener_put_call(items)

    def screener_linkedin(
        self,
        market: str | None = None,
        region: str | None = None,
        limit: int | None = None,
    ) -> Any:
        raw = self.fb.screener.linkedin(
            market=market, region=region, limit=limit, as_dataframe=False
        )
        items = df_to_records_maybe(raw)
        return normalize_screener_linkedin(items)

    # ---------- reddit mentions ----------
    def reddit_mentions_ticker(
        self, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.reddit_mentions.ticker(
            ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_reddit_mentions_ticker(raw)

    def screener_reddit_mentions(
        self,
        market: str | None = None,
        region: str | None = None,
        limit: int | None = None,
    ) -> Any:
        raw = self.fb.screener.reddit_mentions(
            market=market, region=region, limit=limit, as_dataframe=False
        )
        items = df_to_records_maybe(raw.get("data") if isinstance(raw, dict) else raw)
        rows = normalize_screener_reddit_mentions(items)
        summary = normalize_screener_reddit_mentions_summary(
            raw.get("summary") if isinstance(raw, dict) else {}
        )
        return {"rows": rows, "summary": summary}

    def screener_app_ratings(
        self,
        market: str | None = None,
        region: str | None = None,
        limit: int | None = None,
    ) -> Any:
        raw = self.fb.screener.app_ratings(
            market=market, region=region, limit=limit, as_dataframe=False
        )
        items = df_to_records_maybe(raw)
        return normalize_screener_app_ratings(items)
