from __future__ import annotations
from typing import Any, List, Literal
from .utils import df_to_records_maybe
from .normalizers import (
    normalize_available_markets,
    normalize_market_predictions,
    normalize_ticker_predictions,
    normalize_sentiments_ticker,
    normalize_app_ratings_ticker,
    normalize_analyst_ratings_ticker,
    normalize_house_trades_ticker,
    normalize_insider_transactions_ticker,
    normalize_linkedin_ticker,
    normalize_options_put_call_ticker,
)

# SDK import (PyPI package name is finbrain-python; import path is `finbrain`)
from finbrain import FinBrainClient  # type: ignore[import-untyped]


class FBClient:
    """
    Thin wrapper around finbrain-python SDK.
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

    # ---------- app ratings ----------
    def app_ratings_ticker(
        self, market: str, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.app_ratings.ticker(
            market, ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_app_ratings_ticker(raw)

    # ---------- analyst ratings ----------
    def analyst_ratings_ticker(
        self, market: str, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.analyst_ratings.ticker(
            market, ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_analyst_ratings_ticker(raw)

    # ---------- house trades ----------
    def house_trades_ticker(
        self, market: str, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.house_trades.ticker(
            market, ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_house_trades_ticker(raw)

    # ---------- insider transactions ----------
    def insider_transactions_ticker(self, market: str, ticker: str) -> Any:
        raw = self.fb.insider_transactions.ticker(market, ticker, as_dataframe=False)
        return normalize_insider_transactions_ticker(raw)

    # ---------- LinkedIn metrics ----------
    def linkedin_ticker(
        self, market: str, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.linkedin_data.ticker(
            market, ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_linkedin_ticker(raw)

    # ---------- options put/call ----------
    def options_put_call(
        self, market: str, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.options.put_call(
            market, ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_options_put_call_ticker(raw)

    # ---------- price predictions ----------
    def predictions_market(self, market: str) -> Any:
        raw = self.fb.predictions.market(market, as_dataframe=False)
        items = df_to_records_maybe(raw)
        return normalize_market_predictions(items)

    def predictions_ticker(
        self, ticker: str, prediction_type: Literal["daily", "monthly"]
    ) -> Any:
        raw = self.fb.predictions.ticker(
            ticker, prediction_type=prediction_type, as_dataframe=False
        )
        return normalize_ticker_predictions(raw)

    # ---------- news sentiment ----------
    def sentiments_ticker(
        self, market: str, ticker: str, date_from: str | None, date_to: str | None
    ) -> Any:
        raw = self.fb.sentiments.ticker(
            market, ticker, date_from=date_from, date_to=date_to, as_dataframe=False
        )
        return normalize_sentiments_ticker(raw)
