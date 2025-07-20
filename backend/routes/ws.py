from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.ws.connection_manager import active_connections

router = APIRouter()

@router.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keeps connection alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)
