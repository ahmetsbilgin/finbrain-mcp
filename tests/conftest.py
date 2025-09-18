# tests/conftest.py
import pytest

# ---- Fake SDK matching finbrain-python surface (nested namespaces) ----


class _Available:
    def markets(self):
        # RAW shape from your docs
        return {"availableMarkets": ["S&P 500", "NASDAQ"]}

    def tickers(self, dataset: str, as_dataframe: bool = False):
        return [
            {"ticker": "AMZN", "name": "Amazon.com, Inc.", "market": "S&P 500"},
            {"ticker": "AAPL", "name": "Apple Inc.", "market": "S&P 500"},
        ]


class _Predictions:
    def market(self, market: str, as_dataframe: bool = False):
        return [
            {
                "ticker": "STX",
                "name": "Seagate Technology",
                "prediction": {
                    "expectedShort": "1.24632",
                    "expectedMid": "1.34583",
                    "expectedLong": "0.07213",
                    "technicalAnalysis": "…",
                    "lastUpdate": "2020-10-27T23:46:54.359Z",
                    "type": "daily",
                },
                "sentimentScore": "-0.137",
            },
            {
                "ticker": "TAP",
                "name": "Molson Coors Brewing Company",
                "prediction": {
                    "expectedShort": "0.14241",
                    "expectedMid": "1.19539",
                    "expectedLong": "1.34984",
                    "technicalAnalysis": "…",
                    "lastUpdate": "2020-10-27T23:46:54.415Z",
                    "type": "daily",
                },
                "sentimentScore": "0.261",
            },
        ]

    def ticker(
        self, ticker: str, *, prediction_type: str = "daily", as_dataframe: bool = False
    ):
        # echo the requested ticker and type
        daily = {
            "ticker": ticker,
            "name": f"{ticker} Inc.",
            "prediction": {
                "2024-11-04": "201.33,197.21,205.45",
                "2024-11-05": "202.77,196.92,208.61",
                "expectedShort": "0.22",
                "expectedMid": "0.58",
                "expectedLong": "0.25",
                "technicalAnalysis": "…",
                "type": "daily",
                "lastUpdate": "2024-11-01T23:24:18.371Z",
            },
            "sentimentAnalysis": {
                "2024-11-04": "0.186",
                "2024-11-01": "0.339",
            },
        }
        monthly = {
            "ticker": ticker,
            "name": f"{ticker} Inc.",
            "prediction": {
                "2025-01-31": "210.0,190.0,230.0",
                "2025-02-28": "212.0,192.0,232.0",
                "expectedShort": "0.10",
                "expectedMid": "0.40",
                "expectedLong": "0.80",
                "technicalAnalysis": "…",
                "type": "monthly",
                "lastUpdate": "2024-11-01T23:24:18.371Z",
            },
            "sentimentAnalysis": {},
        }
        return monthly if prediction_type == "monthly" else daily


class _Sentiments:
    def ticker(
        self,
        market: str,
        ticker: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
    ):
        return {
            "ticker": ticker,
            "name": "Amazon.com Inc." if ticker == "AMZN" else ticker,
            "sentimentAnalysis": {
                "2021-12-13": "-0.038",
                "2021-12-14": "0.037",
                "2021-12-15": "0.223",
            },
        }


class _AppRatings:
    def ticker(
        self,
        market: str,
        ticker: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
    ):
        return {
            "ticker": ticker,
            "name": "Amazon.com Inc",
            "appRatings": [
                {
                    "playStoreScore": 3.75,
                    "playStoreRatingsCount": 567996,
                    "appStoreScore": 4.07,
                    "appStoreRatingsCount": 88533,
                    "playStoreInstallCount": None,
                    "date": "2024-02-02",
                },
                {
                    "playStoreScore": 3.76,
                    "playStoreRatingsCount": 567421,
                    "appStoreScore": 4.07,
                    "appStoreRatingsCount": 88293,
                    "playStoreInstallCount": None,
                    "date": "2024-01-26",
                },
            ],
        }


class _AnalystRatings:
    def ticker(
        self,
        market: str,
        ticker: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
    ):
        return {
            "ticker": ticker,
            "name": "Amazon.com Inc.",
            "analystRatings": [
                {
                    "date": "2024-02-02",
                    "type": "Reiterated",
                    "institution": "Piper Sandler",
                    "signal": "Neutral",
                    "targetPrice": "$205 → $190",
                },
                {
                    "date": "2024-02-02",
                    "type": "Reiterated",
                    "institution": "Monness Crespi & Hardt",
                    "signal": "Buy",
                    "targetPrice": "$189 → $200",
                },
            ],
        }


class _HouseTrades:
    def ticker(
        self,
        market: str,
        ticker: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
    ):
        return {
            "ticker": ticker,
            "name": "Amazon.com Inc." if ticker == "AMZN" else ticker,
            "houseTrades": [
                {
                    "date": "2024-02-29",
                    "amount": "$360.00",
                    "representative": "Pete Sessions",
                    "type": "Purchase",
                },
                {
                    "date": "2024-01-25",
                    "amount": "$15,001 - $50,000",
                    "representative": "Shri Thanedar",
                    "type": "Sale",
                },
            ],
        }


class _InsiderTransactions:
    def ticker(self, market: str, ticker: str, as_dataframe: bool = False):
        return {
            "ticker": ticker,
            "name": "Amazon.com Inc." if ticker == "AMZN" else ticker,
            "insiderTransactions": [
                {
                    "date": "Mar 08 '24",
                    "insiderTradings": "Selipsky Adam",
                    "relationship": "CEO Amazon Web Services",
                    "transaction": "Sale",
                    "cost": 176.31,
                    "shares": 500,
                    "USDValue": 88155,
                    "totalShares": 133100,
                    "SECForm4Date": "2001-03-11T16:34:00.000Z",
                    "SECForm4Link": "http://www.sec.gov/Archives/edgar/data/1018724/000101872424000058/xslF345X05/wk-form4_1710189274.xml",
                },
                {
                    "date": "Feb 10 '24",
                    "insiderTradings": "Jassy Andrew R",
                    "relationship": "President & CEO",
                    "transaction": "Purchase",
                    "cost": 170.0,
                    "shares": 1000,
                    "USDValue": 170000,
                    "totalShares": 200000,
                    "SECForm4Date": "2001-02-12T10:00:00.000Z",
                    "SECForm4Link": "http://www.sec.gov/some/other/link.xml",
                },
            ],
        }


class _LinkedIn:
    def ticker(
        self,
        market: str,
        ticker: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
    ):
        return {
            "ticker": ticker,
            "name": "Amazon.com Inc." if ticker == "AMZN" else ticker,
            "linkedinData": [
                {
                    "date": "2024-03-20",
                    "employeeCount": 755461,
                    "followersCount": 30628460,
                },
                {
                    "date": "2024-03-27",
                    "employeeCount": 756100,
                    "followersCount": 30690000,
                },
            ],
        }


class _Options:
    def put_call(
        self,
        market: str,
        ticker: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
    ):
        return {
            "ticker": ticker,
            "name": "Amazon.com Inc." if ticker == "AMZN" else ticker,
            "putCallData": [
                {
                    "date": "2024-03-18",
                    "ratio": 0.38,
                    "callCount": 700000,
                    "putCount": 266000,
                },
                {
                    "date": "2024-03-19",
                    "ratio": 0.40,
                    "callCount": 788319,
                    "putCount": 315327,
                },
            ],
        }


class FakeFinBrainSDK:
    def __init__(self, api_key: str):
        self.available = _Available()
        self.predictions = _Predictions()
        self.sentiments = _Sentiments()
        self.app_ratings = _AppRatings()
        self.analyst_ratings = _AnalystRatings()
        self.house_trades = _HouseTrades()
        self.insider_transactions = _InsiderTransactions()
        self.linkedin_data = _LinkedIn()
        self.options = _Options()


@pytest.fixture
def patch_resolvers(monkeypatch):
    """
    Patch per-tool module:
      - make resolve_api_key return a dummy key
      - make the adapter use our Fake SDK (so normalizers run)
    Usage: patch_resolvers(finbrain_mcp.tools.predictions)
    """

    def _apply(module):
        # dummy key
        monkeypatch.setattr(
            module, "resolve_api_key", lambda: "DUMMY-KEY", raising=True
        )
        # patch the SDK used inside the adapter
        import finbrain_mcp.client_adapter as adapter

        monkeypatch.setattr(adapter, "FinBrainClient", FakeFinBrainSDK, raising=True)

    return _apply
