from app.routers import smallcases, tickers
from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def ping():
    return {"data": "pong!"}


app.include_router(tickers.router, prefix="/tickers")
app.include_router(smallcases.router, prefix="/smallcases")
