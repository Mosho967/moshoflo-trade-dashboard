import psycopg2
from faker import Faker
import random
from datetime import datetime, timezone
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai.predictor import classify_trade  

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="moshoflo", user="admin", password="admin", host="localhost", port="5432"
)
cur = conn.cursor()

# Initialize Faker
fake = Faker()

# Sample data options
symbols = ["AAPL", "TSLA", "GOOGL", "AMZN", "MSFT"]
exchanges = ["NYSE", "NASDAQ", "LSE"]
sides = ["BUY", "SELL"]
currencies = ["USD", "GBP", "EUR"]

# Insert 50 fake trades
for _ in range(50):
    trade_id = fake.uuid4()
    symbol = random.choice(symbols)
    price = round(random.uniform(100, 1500), 2)
    volume = round(random.uniform(1, 20000), 2)  # Expanded to trigger MEDIUM/HIGH risk
    side = random.choice(sides)
    exchange = random.choice(exchanges)
    currency = random.choice(currencies)
    timestamp = datetime.now(timezone.utc)
    risk_label = classify_trade(volume)  # Classify risk based on volume

    cur.execute(
        """
        INSERT INTO trades (trade_id, symbol, price, volume, side, exchange, currency, timestamp, risk_label)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (trade_id, symbol, price, volume, side, exchange, currency, timestamp, risk_label),
    )

conn.commit()
cur.close()
conn.close()

print("50 fake trades inserted with risk levels!")
