import argparse
import random
from uuid import uuid4
from datetime import datetime

from backend.db import SessionLocal
from backend.models import Trade


SYMBOLS = ["AAPL", "TSLA", "GOOGL", "AMZN", "MSFT"]
EXCHANGES = ["NYSE", "NASDAQ", "LSE"]
SIDES = ["BUY", "SELL"]
CURRENCIES = ["USD", "GBP", "EUR"]


def seed_trades(n: int):
    db = SessionLocal()

    for _ in range(n):
        trade = Trade(
            trade_id=str(uuid4()),
            symbol=random.choice(SYMBOLS),
            price=round(random.uniform(100, 1500), 2),
            volume=round(random.uniform(1, 20000), 2),
            side=random.choice(SIDES),
            exchange=random.choice(EXCHANGES),
            currency=random.choice(CURRENCIES),
            timestamp=datetime.utcnow(),
        )
        db.add(trade)

    db.commit()
    db.close()

    print(f"Inserted {n} trades.")


def clear_trades():
    db = SessionLocal()
    deleted = db.query(Trade).delete()
    db.commit()
    db.close()

    print(f"Deleted {deleted} trades.")


def main():
    parser = argparse.ArgumentParser(description="Moshoflo CLI")
    subparsers = parser.add_subparsers(dest="command")

    seed_parser = subparsers.add_parser("seed")
    seed_parser.add_argument("--n", type=int, default=50)

    subparsers.add_parser("clear")

    args = parser.parse_args()

    if args.command == "seed":
        seed_trades(args.n)
    elif args.command == "clear":
        clear_trades()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
