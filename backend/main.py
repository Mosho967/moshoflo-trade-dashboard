from fastapi import FastAPI
from backend.routes.trades import router as trades_router
from backend.ws.live_feed import router as ws_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS Middleware — add this!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8000"] for stricter rule
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the trade routes
app.include_router(trades_router)

# Include the WebSocket routes
app.include_router(ws_router)

# Optional root route
@app.get("/")
def read_root():
    return {"status": "Backend is live"}
