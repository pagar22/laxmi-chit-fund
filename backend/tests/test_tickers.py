import pytest


@pytest.mark.asyncio
async def test_get_ticker(test_app, f_ticker_base):
    # Given
    exchnage_token, _ = await f_ticker_base()
    # When
    resp = await test_app.get(url=f"/tickers/{exchnage_token}")
    # Test
    assert resp.status_code == 200
    assert resp.json()["exchange_token"] == exchnage_token


@pytest.mark.asyncio
async def test_get_ticker_not_found(test_app):
    # Given
    exchange_token = "-1"
    # When
    resp = await test_app.get(url=f"/tickers/{exchange_token}")
    # Test
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_ticker_by_smallcase_name(test_app, f_ticker_base):
    # Given
    exchange_token, smallcase_name = await f_ticker_base()
    # When
    resp = await test_app.get(url=f"/tickers/?smallcase_name={smallcase_name}")
    # Test
    assert resp.status_code == 200
    assert resp.json()["exchange_token"] == exchange_token


@pytest.mark.asyncio
async def test_get_ticker_candlesticks(
    test_app, f_ticker_candlestick_payload, f_ticker_candlestick
):
    # Given
    exchange_token = await f_ticker_candlestick()
    candle_dates = list(f_ticker_candlestick_payload["daily"].keys())
    end_date = candle_dates[-1]
    start_date = candle_dates[0]
    # When
    params = {"start_date": start_date, "end_date": end_date}
    resp = await test_app.get(url=f"/tickers/{exchange_token}/candles", params=params)
    # Test
    assert resp.status_code == 200
    assert len(resp.json()) == len(f_ticker_candlestick_payload)
