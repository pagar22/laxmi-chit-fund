from app.daos.tickers import TickerDAO
from app.schemas.tickers import TickerBase
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
tickerDAO = TickerDAO()


@router.get("/{id}")
async def get(ticker: str):
    ticker = await tickerDAO.get(ticker)
    if ticker:
        return ticker
    raise HTTPException(status_code=404, detail="Ticker not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(ticker: TickerBase):
    id = str(ticker.exchange_token)
    await tickerDAO.create(ticker, id)


@router.post("/candle_stick/")
async def create_candle_stick():
    pass
