import pytest
from app.daos.tickers import TickerDAO
from app.schemas.tickers import CandleStickBase, TickerBase


@pytest.fixture(scope="function")
def f_ticker_base_payload(faker):
    return {
        "name": faker.company(),
        "ticker": faker.word(),
        "exchange_token": faker.random_int(min=100, max=999),
        "exchange": "NSE",
        "instrument_type": "EQUITY",
        "smallcase_name": faker.word(),
        "upstox_instrument_key": faker.word(),
        "smallcase_name": faker.word(),
    }


@pytest.fixture(scope="function")
def f_ticker_base(faker, f_ticker_base_payload):
    async def _f_ticker_base():
        dao = TickerDAO()
        id = f_ticker_base_payload["exchange_token"]
        await dao.create(TickerBase(**f_ticker_base_payload), str(id))
        return id, f_ticker_base_payload["smallcase_name"]

    return _f_ticker_base


@pytest.fixture(scope="function")
def f_ticker_candle_stick_payload(faker):
    dates = ["2020-01-01", "2020-01-02", "2020-01-03"]
    daily_data = {
        date: {
            "open": faker.random_int(min=100, max=200),
            "high": faker.random_int(min=100, max=200),
            "low": faker.random_int(min=100, max=200),
            "close": faker.random_int(min=100, max=200),
            "volume": faker.random_int(min=100, max=999),
        }
        for date in dates
    }
    return {
        "month": "01",
        "year": "2020",
        "daily": daily_data,
    }


@pytest.fixture(scope="function")
def f_ticker_candle_stick(faker, f_ticker_base_payload, f_ticker_candle_stick_payload):
    async def _f_ticker_candle_stick():
        dao = TickerDAO()
        id = f_ticker_base_payload["exchange_token"]
        candles = CandleStickBase(**f_ticker_candle_stick_payload)
        await dao.create_candle_sticks(id, candles, "2020-01")
        return id

    return _f_ticker_candle_stick
