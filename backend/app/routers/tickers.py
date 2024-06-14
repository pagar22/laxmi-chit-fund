from app.daos.tickers import TickerDAO
from app.schemas.tickers import CandleBase, CandleStickBase, TickerBase
from app.utils.dates import datestr, split_date, validate_date_range
from fastapi import APIRouter, HTTPException

router = APIRouter()
tickerDAO = TickerDAO()


@router.get("/{id}")
async def get(id: str):
    ticker = await tickerDAO.get(id)
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return ticker


@router.get("/")
async def get_by_smallcase_name(smallcase_name: str):
    ticker = await tickerDAO.get_by_smallcase_name(smallcase_name)
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return ticker


@router.post("/", status_code=201)
async def create(ticker: TickerBase):
    id = str(ticker.exchange_token)
    await tickerDAO.create(ticker, id)


@router.get("/{id}/candles", response_model=dict[str, CandleBase])
async def get_candle_sticks_range(id: str, start_date: str, end_date: str):
    end_date = datestr(end_date)
    start_date = datestr(start_date)
    validate_date_range(start_date, end_date, max_days=366)

    candles = await tickerDAO.get_candle_sticks(id, start_date, end_date)
    if not candles:
        raise HTTPException(status_code=404, detail="Candles not found")
    return candles


@router.get("/{id}/candles/{date}", response_model=CandleStickBase)
async def get_candle_sticks_monthly(id: str, date: str):
    date = datestr(date)
    y, m, d = split_date(date)
    candle = await tickerDAO.get_candle_doc(id, y, m)
    if not candle:
        raise HTTPException(status_code=404, detail="Candles not found")
    return candle


@router.post("/{id}/candles", status_code=201)
async def create_candle_sticks(id: str, candle_sticks: CandleStickBase, date: str):
    date = datestr(date)
    ticker = await tickerDAO.get(id)
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")

    await tickerDAO.create_candle_sticks(id, candle_sticks, date)
