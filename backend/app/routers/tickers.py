from app.daos.tickers import TickerDAO
from app.schemas.tickers import MonthlyCandleBase, TickerBase
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
tickerDAO = TickerDAO()


@router.get("/{id}")
async def get(id: str):
    ticker = await tickerDAO.get(id)
    if ticker:
        return ticker
    raise HTTPException(status_code=404, detail="Ticker not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(ticker: TickerBase):
    id = str(ticker.exchange_token)
    await tickerDAO.create(ticker, id)


@router.post("/{id}/candles", status_code=status.HTTP_201_CREATED)
async def create_candle_sticks(id: str, monthly_candle: MonthlyCandleBase):

    ticker = await tickerDAO.get(id)
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")

    await tickerDAO.create_candle_sticks(id, monthly_candle)
