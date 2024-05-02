from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def ping():
    return {"data": "pong!"}


from app.routers import tickers

app.include_router(tickers.router, prefix="/tickers")
