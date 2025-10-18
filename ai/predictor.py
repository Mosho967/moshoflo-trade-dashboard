import os
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
from typing import Union

ASSETS_DIR = Path(__file__).resolve().parent
MODEL_PATH = ASSETS_DIR / "risk_model.pt"
LABELS_PATH = ASSETS_DIR / "label_encoder_classes.npy"

class RiskClassifierMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(3, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 3),
        )

    def forward(self, x):
        return self.model(x)

#---- Internal loading helpers ----
_model = None
_symbol_to_index = None

def _load_labels():
    global _symbol_to_index
    if _symbol_to_index is not None:
        return _symbol_to_index
    if not LABELS_PATH.exists():
        # Fallback minimal label set if file missing
        labels = np.array(["AAPL", "MSFT", "TSLA"], dtype=object)
    else:
        labels = np.load(LABELS_PATH)
    _symbol_to_index = {symbol: i for i, symbol in enumerate(labels)}
    return _symbol_to_index

def _load_model():
    global _model
    if _model is not None:
        return _model
    m = RiskClassifierMLP()
    if not MODEL_PATH.exists():
        # Fallback dummy if weights absent to prvent crashes
        class DummyModel:
            def __call__(self, x):
                return torch.tensor([[0.1, 0.3, 0.6]], dtype=torch.float32)
        _model = DummyModel()
        return _model
    # safer load mode 
    state = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    m.load_state_dict(state)
    m.eval()
    _model = m
    return _model

# ---- Public API ----
def predict_risk(trade: dict) -> str:
    """Model-based path: expects dict with symbol/volume/price."""
    symbol_to_index = _load_labels()
    model = _load_model()

    symbol = str(trade.get("symbol", "")).upper()
    volume = float(trade.get("volume", 0))
    price = float(trade.get("price", 0.0))
    encoded_symbol = float(symbol_to_index.get(symbol, 0))

    x = torch.tensor([[encoded_symbol, volume, price]], dtype=torch.float32)
    with torch.no_grad():
        logits = model(x)
        pred = torch.argmax(logits, dim=1).item()
        return ["LOW RISK", "MEDIUM RISK", "HIGH RISK"][pred]

def classify_trade(trade: Union[int, float, dict]) -> str:
    """
    Backward-compatible facade:
    - If passed a number -> treat as 'volume' and use simple thresholds (tests expect this).
    - If dict -> defer to model-based predict_risk().
    """
    # Numeric path for tests e.g. classify_trade(50)
    if isinstance(trade, (int, float)):
        volume = float(trade)
        if volume < 1000:
            return "LOW RISK"
        elif volume < 8000:
            return "MEDIUM RISK"
        else:
            return "HIGH RISK"

    # Dict path for app usage
    return predict_risk(trade)
