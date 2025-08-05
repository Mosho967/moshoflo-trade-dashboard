import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os

# Simulate trade data
symbols = ["AAPL", "TSLA", "GOOGL", "AMZN", "MSFT"]
label_encoder = LabelEncoder()
symbol_encoded = label_encoder.fit_transform(symbols)

def generate_data(n=1000):
    import random
    data = []
    for _ in range(n):
        volume = random.randint(10, 10000)
        price = random.uniform(10, 1000)
        symbol = random.choice(symbols)

        if volume > 6000:
            risk = 2  # HIGH RISK
        elif volume > 3000:
            risk = 1  # MEDIUM RISK
        else:
            risk = 0  # LOW RISK

        data.append([symbol, volume, price, risk])
    return data

# Generate and encode data
raw_data = generate_data(1200)
symbol_map = {sym: idx for idx, sym in enumerate(label_encoder.classes_)}

features = []
labels = []

for symbol, volume, price, risk in raw_data:
    features.append([symbol_map[symbol], volume, price])
    labels.append(risk)

X = torch.tensor(features[:1000], dtype=torch.float32)
y = torch.tensor(labels[:1000], dtype=torch.long)

# Define dataset and DataLoader
dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Define model
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

model = RiskClassifierMLP()
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Training loop
model.train()
for epoch in range(20):
    total_loss = 0
    for batch_X, batch_y in dataloader:
        optimizer.zero_grad()
        output = model(batch_X)
        loss = criterion(output, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

# Save model and encoder
os.makedirs("ai", exist_ok=True)
torch.save(model.state_dict(), "ai/risk_model.pt")
np.save("ai/label_encoder_classes.npy", label_encoder.classes_)
print("Trained PyTorch model saved to ai/")
