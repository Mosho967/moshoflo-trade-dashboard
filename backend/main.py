from fastapi import FastAPI
from backend.routes.trades import router as trades_router
from backend.ws.live_feed import router as ws_router
from fastapi.middleware.cors import CORSMiddleware

from backend.db import engine
from backend.models import Base
import backend.models  # ensures model is registered


app = FastAPI()

# Create tables automatically on startup
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the trade routes
app.include_router(trades_router)

# Include the WebSocket routes
app.include_router(ws_router)


# Root
@app.get("/")
def read_root():
    return {"status": "Backend is live"}
