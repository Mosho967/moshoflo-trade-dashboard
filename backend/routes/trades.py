from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from datetime import datetime
import json
from decimal import Decimal

from db import get_db
from models import Trade
from schemas import TradeIn, TradeOut
from ai.predictor import predict_risk
from ws.connection_manager import manager

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.get("/", response_model=list[TradeOut])
def get_all_trades(db: Session = Depends(get_db)):
    trades = db.query(Trade).all()

    out: list[TradeOut] = []
    for t in trades:
        risk_label, _ = predict_risk({
            "symbol": t.symbol,
            "volume": float(t.volume),
            "price": float(t.price),
        })
        out.append(TradeOut(**t.__dict__, risk_label=risk_label))

    return out


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
        timestamp=datetime.utcnow(),
    )

    db.add(new_trade)

    try:
        db.commit()
        db.refresh(new_trade)

        risk_label, _ = predict_risk({
            "symbol": trade.symbol,
            "volume": float(trade.volume),
            "price": float(trade.price),
        })

        trade_out = TradeOut(**new_trade.__dict__, risk_label=risk_label)

        def json_default(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
            return str(obj)

        # Pydantic v2: model_dump() (avoid .dict() going forward)
        await manager.broadcast(json.dumps(trade_out.model_dump(), default=json_default))

        return trade_out

    except SQLAlchemyError as e:
        db.rollback()
        print("DB Error:", repr(e))
        raise HTTPException(status_code=400, detail="Failed to create trade.")
