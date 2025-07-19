import psycopg2
from faker import Faker
import random

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="moshoflo", user="admin", password="pass", host="localhost", port="5432"
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
    volume = round(random.uniform(1, 1000), 2)
    side = random.choice(sides)
    exchange = random.choice(exchanges)
    currency = random.choice(currencies)

    cur.execute(
        """
        INSERT INTO trades (trade_id, symbol, price, volume, side, exchange, currency)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
        (trade_id, symbol, price, volume, side, exchange, currency),
    )

conn.commit()
cur.close()
conn.close()

print(" 50 fake trades inserted!")
