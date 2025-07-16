from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime

# Pydantic schemas for validating and serializing Trade data
class TradeIn(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=10)  # Symbol must be 1–10 characters
    price: Decimal = Field(..., gt=0)                      # Must be greater than 0
    quantity: int = Field(..., gt=0)                       # Must be a positive integer

class TradeOut(TradeIn):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True  # Allows compatibility with SQLAlchemy models
