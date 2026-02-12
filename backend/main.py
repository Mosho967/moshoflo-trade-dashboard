from fastapi import FastAPI
from routes.trades import router as trades_router
from ws.live_feed import router as ws_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

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
