from backend.models import Trade
from backend.db import engine, Base

# Create all tables (no-op if they already exist)
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
