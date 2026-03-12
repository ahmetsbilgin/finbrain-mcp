# tests/conftest.py
import pytest

# ---- Fake SDK matching finbrain-python 0.2.0 surface (v2 API shapes) ----


class _Available:
    def markets(self):
        # V2: list of market objects (SDK unwraps envelope)
        return [{"name": "S&P 500"}, {"name": "NASDAQ"}]

    def tickers(self, prediction_type: str = "daily", as_dataframe: bool = False, **kw):
        return [
            {"symbol": "AMZN", "name": "Amazon.com, Inc.", "market": "S&P 500"},
            {"symbol": "AAPL", "name": "Apple Inc.", "market": "S&P 500"},
        ]

    def regions(self, as_dataframe: bool = False):
        return [
            {"region": "US", "markets": ["S&P 500", "NASDAQ", "DOW 30"]},
            {"region": "UK", "markets": ["UK FTSE 100"]},
        ]


class _News:
    def ticker(
        self,
        symbol: str,
        *,
        date_from=None,
        date_to=None,
        limit=None,
        as_dataframe: bool = False,
    ):
        return {
            "symbol": symbol,
            "name": "Amazon.com Inc." if symbol == "AMZN" else symbol,
            "articles": [
                {
                    "date": "2026-01-19",
                    "headline": "Stock surges on earnings beat",
                    "source": "Reuters",
                    "url": "https://example.com/article1",
                },
                {
                    "date": "2026-01-18",
                    "headline": "Analyst raises price target",
                    "source": "Bloomberg",
                    "url": "https://example.com/article2",
                },
            ],
        }


class _Recent:
    def news(self, *, limit=None, market=None, region=None, as_dataframe=False):
        return [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "date": "2026-01-19",
                "headline": "Apple hits new high",
                "source": "Reuters",
                "url": "https://example.com/apple",
            },
            {
                "symbol": "MSFT",
                "name": "Microsoft Corp.",
                "date": "2026-01-19",
                "headline": "Microsoft AI push continues",
                "source": "Bloomberg",
                "url": "https://example.com/msft",
            },
        ]

    def analyst_ratings(self, *, limit=None, market=None, region=None, as_dataframe=False):
        return [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "date": "2026-01-19",
                "institution": "Goldman Sachs",
                "action": "Upgraded",
                "rating": "Buy",
                "targetPrice": "$250",
            },
        ]


class _Screener:
    def predictions_daily(self, *, market=None, region=None, limit=None, as_dataframe=False):
        return [
            {
                "symbol": "STX",
                "name": "Seagate Technology",
                "expectedShortTerm": 1.24632,
                "expectedMidTerm": 1.34583,
                "expectedLongTerm": 0.07213,
                "lastUpdated": "2020-10-27T23:46:54.359Z",
            },
            {
                "symbol": "TAP",
                "name": "Molson Coors Brewing Company",
                "expectedShortTerm": 0.14241,
                "expectedMidTerm": 1.19539,
                "expectedLongTerm": 1.34984,
                "lastUpdated": "2020-10-27T23:46:54.415Z",
            },
        ]

    def predictions_monthly(self, *, market=None, region=None, limit=None, as_dataframe=False):
        return self.predictions_daily(
            market=market, region=region, limit=limit, as_dataframe=as_dataframe
        )

    def sentiment(self, *, limit=None, market=None, region=None, as_dataframe=False):
        return [
            {"symbol": "AAPL", "name": "Apple Inc.", "date": "2026-01-19", "score": 0.45},
            {"symbol": "MSFT", "name": "Microsoft Corp.", "date": "2026-01-19", "score": -0.12},
        ]

    def analyst_ratings(self, *, limit=None, market=None, region=None, as_dataframe=False):
        return [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "date": "2026-01-19",
                "institution": "Morgan Stanley",
                "action": "Reiterated",
                "rating": "Overweight",
                "targetPrice": "$230",
            },
        ]

    def insider_trading(self, *, limit=None, as_dataframe=False):
        return [
            {
                "symbol": "AMZN",
                "name": "Amazon.com Inc.",
                "date": "2026-01-15",
                "insider": "Jassy Andrew R",
                "relationship": "CEO",
                "transactionType": "Sale",
                "shares": 5000,
                "totalValue": 950000,
            },
        ]

    def congress_house(self, *, limit=None, as_dataframe=False):
        return [
            {
                "symbol": "NVDA",
                "name": "NVIDIA Corp.",
                "date": "2026-01-10",
                "politician": "Nancy Pelosi",
                "transactionType": "Purchase",
                "amount": "$1,000,001 - $5,000,000",
            },
        ]

    def congress_senate(self, *, limit=None, as_dataframe=False):
        return [
            {
                "symbol": "MSFT",
                "name": "Microsoft Corp.",
                "date": "2026-01-12",
                "politician": "Tommy Tuberville",
                "transactionType": "Purchase",
                "amount": "$50,001 - $100,000",
            },
        ]

    def news(self, *, limit=None, market=None, region=None, as_dataframe=False):
        return [
            {
                "symbol": "TSLA",
                "name": "Tesla Inc.",
                "date": "2026-01-19",
                "headline": "Tesla expands production",
                "source": "CNBC",
                "url": "https://example.com/tsla",
            },
        ]

    def put_call_ratio(self, *, limit=None, market=None, region=None, as_dataframe=False):
        return [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "date": "2026-01-19",
                "ratio": 0.65,
                "callVolume": 500000,
                "putVolume": 325000,
            },
        ]

    def linkedin(self, *, limit=None, market=None, region=None, as_dataframe=False):
        return [
            {
                "symbol": "AMZN",
                "name": "Amazon.com Inc.",
                "date": "2026-01-19",
                "employeeCount": 1500000,
                "followerCount": 35000000,
                "jobCount": 12000,
            },
        ]

    def app_ratings(self, *, limit=None, market=None, region=None, as_dataframe=False):
        return [
            {
                "symbol": "AMZN",
                "name": "Amazon.com Inc.",
                "date": "2026-01-19",
                "iosRating": 4.7,
                "androidRating": 4.3,
            },
        ]


class _Predictions:
    def ticker(
        self, symbol: str, *, prediction_type: str = "daily", as_dataframe: bool = False
    ):
        # V2 shape (SDK unwraps envelope, returns data field)
        daily = {
            "symbol": symbol,
            "name": f"{symbol} Inc.",
            "type": "daily",
            "predictions": [
                {"date": "2024-11-04", "mid": 201.33, "lower": 197.21, "upper": 205.45},
                {"date": "2024-11-05", "mid": 202.77, "lower": 196.92, "upper": 208.61},
            ],
            "metadata": {
                "expectedShortTerm": 0.22,
                "expectedMidTerm": 0.58,
                "expectedLongTerm": 0.25,
            },
            "lastUpdated": "2024-11-01T23:24:18.371Z",
        }
        monthly = {
            "symbol": symbol,
            "name": f"{symbol} Inc.",
            "type": "monthly",
            "predictions": [
                {"date": "2025-01-31", "mid": 210.0, "lower": 190.0, "upper": 230.0},
                {"date": "2025-02-28", "mid": 212.0, "lower": 192.0, "upper": 232.0},
            ],
            "metadata": {
                "expectedShortTerm": 0.10,
                "expectedMidTerm": 0.40,
                "expectedLongTerm": 0.80,
            },
            "lastUpdated": "2024-11-01T23:24:18.371Z",
        }
        return monthly if prediction_type == "monthly" else daily


class _Sentiments:
    def ticker(
        self,
        symbol: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
        **kw,
    ):
        # V2: data is an array of {date, score}
        return {
            "symbol": symbol,
            "name": "Amazon.com Inc." if symbol == "AMZN" else symbol,
            "data": [
                {"date": "2021-12-13", "score": -0.038},
                {"date": "2021-12-14", "score": 0.037},
                {"date": "2021-12-15", "score": 0.223},
            ],
        }


class _AppRatings:
    def ticker(
        self,
        symbol: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
        **kw,
    ):
        # V2: nested ios/android objects
        return {
            "symbol": symbol,
            "name": "Amazon.com Inc",
            "data": [
                {
                    "date": "2024-02-02",
                    "ios": {"score": 4.07, "ratingsCount": 88533},
                    "android": {
                        "score": 3.75,
                        "ratingsCount": 567996,
                        "installCount": None,
                    },
                },
                {
                    "date": "2024-01-26",
                    "ios": {"score": 4.07, "ratingsCount": 88293},
                    "android": {
                        "score": 3.76,
                        "ratingsCount": 567421,
                        "installCount": None,
                    },
                },
            ],
        }


class _AnalystRatings:
    def ticker(
        self,
        symbol: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
        **kw,
    ):
        # V2: ratings array with action/rating instead of type/signal
        return {
            "symbol": symbol,
            "name": "Amazon.com Inc.",
            "ratings": [
                {
                    "date": "2024-02-02",
                    "institution": "Piper Sandler",
                    "action": "Reiterated",
                    "rating": "Neutral",
                    "targetPrice": "$205 \u2192 $190",
                },
                {
                    "date": "2024-02-02",
                    "institution": "Monness Crespi & Hardt",
                    "action": "Reiterated",
                    "rating": "Buy",
                    "targetPrice": "$189 \u2192 $200",
                },
            ],
        }


class _HouseTrades:
    def ticker(
        self,
        symbol: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
        **kw,
    ):
        # V2: trades array with politician/transactionType
        return {
            "symbol": symbol,
            "name": "Amazon.com Inc." if symbol == "AMZN" else symbol,
            "chamber": "house",
            "trades": [
                {
                    "date": "2024-02-29",
                    "amount": "$360.00",
                    "politician": "Pete Sessions",
                    "transactionType": "Purchase",
                },
                {
                    "date": "2024-01-25",
                    "amount": "$15,001 - $50,000",
                    "politician": "Shri Thanedar",
                    "transactionType": "Sale",
                },
            ],
        }


class _SenateTrades:
    def ticker(
        self,
        symbol: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
        **kw,
    ):
        # V2: trades array with politician/transactionType
        return {
            "symbol": symbol,
            "name": "Meta Platforms Inc." if symbol == "META" else symbol,
            "chamber": "senate",
            "trades": [
                {
                    "date": "2025-11-13",
                    "amount": "$1,001 - $15,000",
                    "politician": "Shelley Moore Capito",
                    "transactionType": "Purchase",
                },
                {
                    "date": "2025-10-31",
                    "amount": "$1,001 - $15,000",
                    "politician": "John Boozman",
                    "transactionType": "Purchase",
                },
            ],
        }


class _CorporateLobbying:
    def ticker(
        self,
        symbol: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
        **kw,
    ):
        # V2: filings array with lobbying data
        return {
            "symbol": symbol,
            "name": "Apple Inc." if symbol == "AAPL" else symbol,
            "filings": [
                {
                    "date": "2024-01-15",
                    "filingUuid": "uuid-001",
                    "filingYear": 2024,
                    "quarter": "Q1",
                    "clientName": "Apple Inc.",
                    "registrantName": "Fierce Government Relations",
                    "income": 150000,
                    "expenses": 120000,
                    "issueCodes": ["TAX", "TEC"],
                    "governmentEntities": ["U.S. Senate", "U.S. House of Representatives"],
                },
                {
                    "date": "2023-10-20",
                    "filingUuid": "uuid-002",
                    "filingYear": 2023,
                    "quarter": "Q4",
                    "clientName": "Apple Inc.",
                    "registrantName": "Franklin Square Group",
                    "income": 200000,
                    "expenses": 180000,
                    "issueCodes": ["CPT", "IMM"],
                    "governmentEntities": ["U.S. Senate"],
                },
            ],
        }


class _InsiderTransactions:
    def ticker(
        self,
        symbol: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
        **kw,
    ):
        # V2: transactions array with ISO dates and new field names
        return {
            "symbol": symbol,
            "name": "Amazon.com Inc." if symbol == "AMZN" else symbol,
            "transactions": [
                {
                    "date": "2024-03-08",
                    "insider": "Selipsky Adam",
                    "relationship": "CEO Amazon Web Services",
                    "transactionType": "Sale",
                    "shares": 500,
                    "pricePerShare": 176.31,
                    "totalValue": 88155,
                    "sharesOwned": 133100,
                    "filingDate": "2024-03-11",
                    "filingUrl": "http://www.sec.gov/Archives/edgar/data/1018724/000101872424000058/xslF345X05/wk-form4_1710189274.xml",
                },
                {
                    "date": "2024-02-10",
                    "insider": "Jassy Andrew R",
                    "relationship": "President & CEO",
                    "transactionType": "Purchase",
                    "shares": 1000,
                    "pricePerShare": 170.0,
                    "totalValue": 170000,
                    "sharesOwned": 200000,
                    "filingDate": "2024-02-12",
                    "filingUrl": "http://www.sec.gov/some/other/link.xml",
                },
            ],
        }


class _LinkedIn:
    def ticker(
        self,
        symbol: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
        **kw,
    ):
        # V2: data array with followerCount (not followersCount)
        return {
            "symbol": symbol,
            "name": "Amazon.com Inc." if symbol == "AMZN" else symbol,
            "data": [
                {
                    "date": "2024-03-20",
                    "employeeCount": 755461,
                    "followerCount": 30628460,
                    "jobCount": None,
                },
                {
                    "date": "2024-03-27",
                    "employeeCount": 756100,
                    "followerCount": 30690000,
                    "jobCount": None,
                },
            ],
        }


class _Options:
    def put_call(
        self,
        symbol: str,
        date_from=None,
        date_to=None,
        as_dataframe: bool = False,
        **kw,
    ):
        # V2: data array with callVolume/putVolume (not callCount/putCount)
        return {
            "symbol": symbol,
            "name": "Amazon.com Inc." if symbol == "AMZN" else symbol,
            "data": [
                {
                    "date": "2024-03-18",
                    "ratio": 0.38,
                    "callVolume": 700000,
                    "putVolume": 266000,
                    "totalVolume": 966000,
                    "price": 180.50,
                },
                {
                    "date": "2024-03-19",
                    "ratio": 0.40,
                    "callVolume": 788319,
                    "putVolume": 315327,
                    "totalVolume": 1103646,
                    "price": 181.20,
                },
            ],
        }


class FakeFinBrainSDK:
    def __init__(self, api_key: str):
        self.available = _Available()
        self.screener = _Screener()
        self.predictions = _Predictions()
        self.sentiments = _Sentiments()
        self.app_ratings = _AppRatings()
        self.analyst_ratings = _AnalystRatings()
        self.house_trades = _HouseTrades()
        self.senate_trades = _SenateTrades()
        self.corporate_lobbying = _CorporateLobbying()
        self.insider_transactions = _InsiderTransactions()
        self.linkedin_data = _LinkedIn()
        self.options = _Options()
        self.news = _News()
        self.recent = _Recent()


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
