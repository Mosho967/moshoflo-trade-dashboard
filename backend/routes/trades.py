from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from datetime import datetime
import json
from decimal import Decimal

from backend.db import get_db
from backend.models import Trade
from backend.schemas import TradeIn, TradeOut
from ai.predictor import predict_risk  # 🔁 now using ML model
from backend.ws.connection_manager import manager  

router = APIRouter(
    prefix="/trades",
    tags=["Trades"]
)

# GET all trades
@router.get("/", response_model=list[TradeOut])
def get_all_trades(db: Session = Depends(get_db)):
    trades = db.query(Trade).all()
    return [
        TradeOut(**t.__dict__, risk_label=predict_risk({
            "symbol": t.symbol,
            "volume": float(t.volume),
            "price": float(t.price)
        }))
        for t in trades
    ]

# POST a new trade
@router.post("/", response_model=TradeOut)
async def create_trade(trade: TradeIn, db: Session = Depends(get_db)):
    new_trade = Trade(
        trade_id=str(uuid4()),
        symbol=trade.symbol,
        price=trade.price,
        volume=trade.volume,
        side=trade.side,
        exchange=trade.exchange,
        currency=trade.currency,
        timestamp=datetime.utcnow()
    )

    db.add(new_trade)

    try:
        db.commit()
        db.refresh(new_trade)

        trade_out = TradeOut(**new_trade.__dict__)
        trade_out.risk_label = predict_risk({
            "symbol": trade.symbol,
            "volume": float(trade.volume),
            "price": float(trade.price)
        })

        def decimal_to_float(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
            return str(obj)

        await manager.broadcast(json.dumps(trade_out.dict(), default=decimal_to_float))

        return trade_out

    except SQLAlchemyError as e:
        db.rollback()
        print("DB Error:", e)
        raise HTTPException(status_code=400, detail="Failed to create trade.")
