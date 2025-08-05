import torch
import torch.nn as nn
import numpy as np
import os

class RiskClassifierMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(3, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 3)
        )

    def forward(self, x):
        return self.model(x)

# Load model and encoder
model = RiskClassifierMLP()
model_path = os.path.join(os.path.dirname(__file__), "risk_model.pt")
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

label_path = os.path.join(os.path.dirname(__file__), "label_encoder_classes.npy")
label_classes = np.load(label_path)
symbol_to_index = {symbol: i for i, symbol in enumerate(label_classes)}

def predict_risk(trade: dict) -> str:
    symbol = trade.get("symbol", "").upper()
    volume = trade.get("volume", 0)
    price = trade.get("price", 0.0)
    encoded_symbol = symbol_to_index.get(symbol, 0)
    input_tensor = torch.tensor([[encoded_symbol, volume, price]], dtype=torch.float32)
    with torch.no_grad():
        logits = model(input_tensor)
        predicted_class = torch.argmax(logits, dim=1).item()
    # return ["LOW RISK", "MEDIUM RISK", "HIGH RISK"][predicted_class]
