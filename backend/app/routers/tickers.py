from app.daos.tickers import TickerDAO
from app.schemas.tickers import CandleStickBase, TickerBase
from app.utils.validators import datestr, get_days_between_dates
from fastapi import APIRouter, HTTPException

router = APIRouter()
tickerDAO = TickerDAO()


@router.get("/{id}")
async def get(id: str):
    ticker = await tickerDAO.get(id)
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return ticker


@router.post("/", status_code=201)
async def create(ticker: TickerBase):
    id = str(ticker.exchange_token)
    await tickerDAO.create(ticker, id)


@router.get("/{id}/candles")
async def get_candle_sticks(id: str, start_date: str, end_date: str):
    start_date = datestr(start_date)
    end_date = datestr(end_date)
    days = get_days_between_dates(start_date, end_date)
    if days <= 0:
        raise HTTPException(status_code=400, detail="Invalid date range")
    elif days > 365:
        raise HTTPException(
            status_code=400, detail="Cannot fetch candles for more than 1 year"
        )

    candles = await tickerDAO.get_candle_sticks(id, start_date, end_date)
    if not candles:
        raise HTTPException(status_code=404, detail="Candles not found")
    return candles


@router.post("/{id}/candles", status_code=201)
async def create_candle_sticks(id: str, candle_sticks: CandleStickBase, date: str):
    date = datestr(date)
    ticker = await tickerDAO.get(id)
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")

    await tickerDAO.create_candle_sticks(id, candle_sticks, date)
