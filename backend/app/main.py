from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import health, deck

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = FastAPI(title="ShipDeck API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(deck.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to ShipDeck API"}
