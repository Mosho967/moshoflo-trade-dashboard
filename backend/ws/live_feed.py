from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from ws.connection_manager import manager

router = APIRouter()

@router.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send heartbeat every 25s to keep proxies from killing idle connections
            await websocket.send_text('{"type":"heartbeat"}')
            await asyncio.sleep(25)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
