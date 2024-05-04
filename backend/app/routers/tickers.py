from app.daos.tickers import TickerDAO
from app.schemas.tickers import TickerBase
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get():
    tickerDAO = TickerDAO()
    return {"model": tickerDAO.model}


@router.post("/")
async def create(ticker: TickerBase):
    tickerDAO = TickerDAO()
    await tickerDAO.create(ticker)
