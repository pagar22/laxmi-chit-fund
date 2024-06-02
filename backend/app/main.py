from app.internal.middelware import app_middleware
from app.routers import smallcases, tickers
from fastapi import FastAPI

app = FastAPI()


@app.get("/ping", tags=["Health"])
def ping():
    return {"data": "pong!"}


app.include_router(tickers.router, prefix="/tickers", tags=["Tickers"])
app.include_router(smallcases.router, prefix="/smallcases", tags=["Smallcases"])

# Middelware
app_middleware(app)
