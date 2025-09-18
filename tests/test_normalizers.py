from finbrain_mcp.normalizers import (
    normalize_available_markets,
    normalize_market_predictions,
    normalize_ticker_predictions,
)


def test_normalize_available_markets():
    assert normalize_available_markets({"availableMarkets": ["S&P 500", "NASDAQ"]}) == [
        "S&P 500",
        "NASDAQ",
    ]
    assert normalize_available_markets(["A", "B"]) == ["A", "B"]
    assert normalize_available_markets(None) == []


def test_normalize_market_predictions():
    raw = [
        {
            "ticker": "STX",
            "name": "Seagate Technology",
            "prediction": {
                "expectedShort": "1.0",
                "expectedMid": "2.0",
                "expectedLong": "3.0",
                "technicalAnalysis": "ta",
                "lastUpdate": "2020-01-01T00:00:00Z",
                "type": "daily",
            },
            "sentimentScore": "-0.5",
        }
    ]
    rows = normalize_market_predictions(raw)
    r = rows[0]
    assert r["expected_short"] == "1.00%"
    assert r["sentiment_score"] == -0.5
    assert r["technical_analysis"] == "ta"


def test_normalize_ticker_predictions():
    raw = {
        "ticker": "AAPL",
        "name": "Apple",
        "prediction": {
            "2024-11-04": "201.33,197.21,205.45",
            "expectedShort": "0.22",
            "expectedMid": "0.58",
            "expectedLong": "0.25",
            "technicalAnalysis": "ta",
            "type": "daily",
            "lastUpdate": "2024-11-01T00:00:00Z",
        },
        "sentimentAnalysis": {"2024-11-04": "0.186"},
    }
    obj = normalize_ticker_predictions(raw)
    assert obj["expected_mid"] == "0.58%"
    assert obj["series"][0]["mid"] == 201.33
    assert obj["sentiment"][0]["score"] == 0.186
