from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.db import get_db
from backend.models import Trade
from backend.schemas import TradeIn, TradeOut

router = APIRouter(
    prefix="/trades",
    tags=["Trades"]
)

# GET all trades
@router.get("/", response_model=list[TradeOut])
def get_all_trades(db: Session = Depends(get_db)):
    trades = db.query(Trade).all()
    return trades

# POST a new trade
@router.post("/", response_model=TradeOut)
def create_trade(trade: TradeIn, db: Session = Depends(get_db)):
    new_trade = Trade(**trade.dict())
    db.add(new_trade)
    try:
        db.commit()
        db.refresh(new_trade)
        return new_trade
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create trade.")
