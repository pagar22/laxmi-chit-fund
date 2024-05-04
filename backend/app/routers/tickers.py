from app.daos.tickers import TickerDAO
from app.schemas.tickers import TickerBase
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("/{id}")
async def get(ticker: str):
    tickerDAO = TickerDAO()
    ticker = await tickerDAO.get(ticker)
    if ticker:
        return ticker
    raise HTTPException(status_code=404, detail="Ticker not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(ticker: TickerBase):
    tickerDAO = TickerDAO()
    id = str(ticker.exchange_token)
    await tickerDAO.create(ticker, id)
