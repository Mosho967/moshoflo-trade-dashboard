from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.ws.connection_manager import manager

router = APIRouter()

# WebSocket endpoint for live trade feed
@router.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keeps the connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)
