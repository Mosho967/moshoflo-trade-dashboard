from joblib import load
import os

# Load model and encoder
model_path = os.path.join(os.path.dirname(__file__), "risk_model.joblib")
encoder_path = os.path.join(os.path.dirname(__file__), "label_encoder.joblib")

model = load(model_path)
label_encoder = load(encoder_path)

def predict_risk(trade: dict) -> str:
    """
    Predicts the risk level of a trade using the trained model.
    trade = {
        "symbol": "AAPL",
        "volume": 2000,
        "price": 250.5
    }
    """
    symbol_encoded = label_encoder.transform([trade["symbol"]])[0]
    features = [[symbol_encoded, trade["volume"], trade["price"]]]
    prediction = model.predict(features)
    return prediction[0]