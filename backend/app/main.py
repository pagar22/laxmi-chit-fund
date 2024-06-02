from app.internal.middelware import app_middleware
from app.routers import internal, smallcases, tickers
from fastapi import FastAPI

app = FastAPI()

app.include_router(internal.router)
app.include_router(tickers.router, prefix="/tickers", tags=["Tickers"])
app.include_router(smallcases.router, prefix="/smallcases", tags=["Smallcases"])

# Middelware
app_middleware(app)
