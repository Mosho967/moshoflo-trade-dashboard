from sqlalchemy import Column, String, Numeric, DateTime, Integer
from backend.db import Base
from datetime import datetime

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    trade_id = Column(String(52), unique=True, nullable=False)
    symbol = Column(String(15), nullable=False)
    price = Column(Numeric(14, 4), nullable=False)
    volume = Column(Numeric(14, 4), nullable=False)
    side = Column(String(4), nullable=False)
    exchange = Column(String(50), nullable=False)
    currency = Column(String(10)) 
    timestamp = Column(DateTime, default=datetime.utcnow) 
