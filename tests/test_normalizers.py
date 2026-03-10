from finbrain_mcp.normalizers import (
    normalize_available_markets,
    normalize_screener_predictions,
    normalize_ticker_predictions,
)


def test_normalize_available_markets():
    # V2: list of dicts
    assert normalize_available_markets([{"name": "S&P 500"}, {"name": "NASDAQ"}]) == [
        "S&P 500",
        "NASDAQ",
    ]
    # fallback: already a list of strings
    assert normalize_available_markets(["A", "B"]) == ["A", "B"]
    assert normalize_available_markets(None) == []


def test_normalize_screener_predictions():
    raw = [
        {
            "symbol": "STX",
            "name": "Seagate Technology",
            "expectedShortTerm": 1.0,
            "expectedMidTerm": 2.0,
            "expectedLongTerm": 3.0,
            "lastUpdated": "2020-01-01T00:00:00Z",
        }
    ]
    rows = normalize_screener_predictions(raw)
    r = rows[0]
    assert r["expected_short"] == "1.00%"
    assert r["expected_mid"] == "2.00%"
    assert r["ticker"] == "STX"
    assert r["last_update"] == "2020-01-01T00:00:00Z"


def test_normalize_ticker_predictions():
    raw = {
        "symbol": "AAPL",
        "name": "Apple",
        "type": "daily",
        "predictions": [
            {"date": "2024-11-04", "mid": 201.33, "lower": 197.21, "upper": 205.45},
        ],
        "metadata": {
            "expectedShortTerm": 0.22,
            "expectedMidTerm": 0.58,
            "expectedLongTerm": 0.25,
        },
        "lastUpdated": "2024-11-01T00:00:00Z",
    }
    obj = normalize_ticker_predictions(raw)
    assert obj["expected_mid"] == "0.58%"
    assert obj["series"][0]["mid"] == 201.33
    assert obj["series"][0]["low"] == 197.21
    assert obj["series"][0]["high"] == 205.45
    assert obj["ticker"] == "AAPL"
