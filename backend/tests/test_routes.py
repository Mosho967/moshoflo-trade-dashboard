from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_get_all_trades():
    response = client.get("/trades/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_trade():
    trade_data = {
        "symbol": "AAPL",
        "price": 123.45,
        "volume": 1000,
        "side": "BUY",
        "exchange": "NASDAQ",
        "currency": "USD",
    }
    response = client.post("/trades/", json=trade_data)
    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "AAPL"
    assert body["side"] == "BUY"
    assert "risk_label" in body
