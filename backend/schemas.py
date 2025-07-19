from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional



# Enum for trade side (BUY or SELL)
class SideEnum(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


# Pydantic schemas for validating and serializing Trade data
class TradeIn(BaseModel):
    symbol: str = Field(..., max_length=15)
    price: Decimal = Field(..., gt=0)
    volume: Decimal = Field(..., gt=0)
    side: SideEnum
    exchange: str = Field(..., max_length=50)
    currency: str | None = Field(None, max_length=10)


class TradeOut(TradeIn):
    id: int
    trade_id: str
    timestamp: Optional[datetime]  # allow None
    risk_label: Optional[str] = None

    class Config:
        from_attributes = True
