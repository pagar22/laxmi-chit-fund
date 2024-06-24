import pytest


@pytest.mark.asyncio
async def test_get_ticker(test_app, f_ticker_base):
    # Given
    exchnage_token = await f_ticker_base()
    # When
    resp = await test_app.get(url=f"/tickers/{exchnage_token}")
    # Test
    assert resp.status_code == 200
    assert resp.json()["exchange_token"] == exchnage_token
