from app.routers import tickers
from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def ping():
    return {"data": "pong!"}


app.include_router(tickers.router, prefix="/tickers")
