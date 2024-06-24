import pytest
from app.daos.tickers import TickerDAO
from app.schemas.tickers import TickerBase


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
    }


@pytest.fixture(scope="function")
def f_ticker_base(faker, f_ticker_base_payload):
    async def _f_ticker_base():
        nonlocal faker, f_ticker_base_payload
        dao = TickerDAO()
        id = f_ticker_base_payload["exchange_token"]
        await dao.create(TickerBase(**f_ticker_base_payload), str(id))
        return id

    return _f_ticker_base
