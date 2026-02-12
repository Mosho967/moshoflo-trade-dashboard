from pathlib import Path
from typing import Union, Tuple

import numpy as np

# --- Optional Torch import ---
try:
    import torch
    import torch.nn as nn
except ImportError:
    torch = None
    nn = None

TORCH_AVAILABLE = (torch is not None) and (nn is not None)

ASSETS_DIR = Path(__file__).resolve().parent
MODEL_PATH = ASSETS_DIR / "risk_model.pt"
LABELS_PATH = ASSETS_DIR / "label_encoder_classes.npy"

# ---- Model definition ----
if TORCH_AVAILABLE:
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
else:
    RiskClassifierMLP = None

# ---- Internal cached state ----
_model = None
_symbol_to_index = None


def _load_labels() -> dict:
    """Loads symbol->index mapping (cached)."""
    global _symbol_to_index
    if _symbol_to_index is not None:
        return _symbol_to_index

    if LABELS_PATH.exists():
        labels = np.load(LABELS_PATH, allow_pickle=True)
    else:
        labels = np.array(["AAPL", "MSFT", "TSLA"], dtype=object)

    _symbol_to_index = {str(symbol).upper(): i for i, symbol in enumerate(labels)}
    return _symbol_to_index


def _heuristic_risk(symbol: str, volume: float, price: float) -> str:
    """
    Cheap fallback that keeps API alive when ML isn't available.
    """
    if volume >= 8000 or price >= 1000:
        return "HIGH RISK"
    if volume >= 1000:
        return "MEDIUM RISK"
    return "LOW RISK"


def _load_model():
    """Loads torch model once (cached). Returns None if unavailable."""
    global _model

    if not TORCH_AVAILABLE or RiskClassifierMLP is None:
        return None

    if _model is not None:
        return _model

    if not MODEL_PATH.exists():
        return None

    m = RiskClassifierMLP()
    try:
        # torch>=2.0 supports weights_only 
        try:
            state = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
        except TypeError:
            state = torch.load(MODEL_PATH, map_location="cpu")

        m.load_state_dict(state)
        m.eval()
        _model = m
        return _model

    except Exception:
        # Any load failure, no ML
        return None


def predict_risk(trade: dict) -> Tuple[str, str]:
    """
    Returns: (risk_label, risk_source)
    risk_source is "ml" or "heuristic"
    """
    symbol_to_index = _load_labels()

    symbol = str(trade.get("symbol", "")).upper()
    volume = float(trade.get("volume", 0))
    price = float(trade.get("price", 0.0))

    # No torch in env - heuristic
    if not TORCH_AVAILABLE:
        return _heuristic_risk(symbol, volume, price), "heuristic"

    model = _load_model()
    if model is None:
        return _heuristic_risk(symbol, volume, price), "heuristic"

    encoded_symbol = float(symbol_to_index.get(symbol, 0))
    x = torch.tensor([[encoded_symbol, volume, price]], dtype=torch.float32)

    try:
        with torch.no_grad():
            logits = model(x)
            pred = int(torch.argmax(logits, dim=1).item())
        return ["LOW RISK", "MEDIUM RISK", "HIGH RISK"][pred], "ml"
    except Exception:
        # Any inference failure - heuristic
        return _heuristic_risk(symbol, volume, price), "heuristic"


def classify_trade(trade: Union[int, float, dict]) -> str:
    """
    Backward-compatible facade for tests:
    - number => threshold classification
    - dict => predict_risk
    """
    if isinstance(trade, (int, float)):
        volume = float(trade)
        if volume < 1000:
            return "LOW RISK"
        elif volume < 8000:
            return "MEDIUM RISK"
        else:
            return "HIGH RISK"

    label, _source = predict_risk(trade)
    return label
