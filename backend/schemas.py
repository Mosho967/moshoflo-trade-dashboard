from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum  

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
    risk_label: str | None = None
    trade_id: str
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True