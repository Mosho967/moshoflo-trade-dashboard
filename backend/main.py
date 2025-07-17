from fastapi import FastAPI
from backend.routes.trades import router as trades_router

app = FastAPI()

# Include the trade routes
app.include_router(trades_router)

# Optional root route
@app.get("/")
def read_root():
    return {"status": "Backend is live"}
