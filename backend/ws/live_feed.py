from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

active_connections: List[WebSocket] = []


# WebSocket endpoint for live trade feed
@router.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep the connection open
    except WebSocketDisconnect:
        active_connections.remove(websocket)
