import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from joblib import dump

# Generated dummy trades
def generate_data(n=1000):
    import random

    data = []
    symbols = ["AAPL", "TSLA", "GOOGL", "AMZN", "MSFT"]
    for _ in range(n):
        volume = random.randint(10, 10000)
        price = random.uniform(10, 1000)
        symbol = random.choice(symbols)

        if volume > 6000:
            risk = "HIGH RISK"
        elif volume > 3000:
            risk = "MEDIUM RISK"
        else:
            risk = "LOW RISK"

        data.append([symbol, volume, price, risk])
    return pd.DataFrame(data, columns=["symbol", "volume", "price", "risk_label"])

# Create dataset
df = generate_data()

# Encode symbols
label_encoder = LabelEncoder()
df["symbol_encoded"] = label_encoder.fit_transform(df["symbol"])

# Split data
X = df[["symbol_encoded", "volume", "price"]]
y = df["risk_label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model & encoder
dump(model, "ai/risk_model.joblib")
dump(label_encoder, "ai/label_encoder.joblib")

print("Model trained and saved in ai/ folder.")
