from fastapi import FastAPI
from backend.app.api import health, deck

app = FastAPI(title="ShipDeck API", version="1.0")

app.include_router(health.router, prefix="/api")
app.include_router(deck.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to ShipDeck API"}
