import pytest


@pytest.mark.asyncio
async def test_get_smallcase(test_app, f_smallcase):
    # Given
    id = await f_smallcase()
    # When
    resp = await test_app.get(url=f"/smallcases/{id}")
    # Test
    assert resp.status_code == 200
    assert resp.json()["id"] == id


@pytest.mark.asyncio
async def test_get_smallcase_not_found(test_app):
    # Given
    id = "abc"
    # When
    resp = await test_app.get(url=f"/smallcases/{id}")
    # Test
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_smallcase_constituents(test_app, f_smallcase_constituents):
    # Given
    id, constituents = await f_smallcase_constituents()
    date = constituents["start_date"]
    # When
    params = {"date": date}
    resp = await test_app.get(url=f"/smallcases/{id}/constituents", params=params)
    # Test
    assert resp.status_code == 200
    assert len(resp.json()["constituents"]) == len(constituents["constituents"])


@pytest.mark.asyncio
async def test_get_smallcase_constituents_stream(test_app, f_smallcase_constituents):
    # Given
    id, constituents = await f_smallcase_constituents()
    # When
    resp = await test_app.get(url=f"/smallcases/{id}/constituents/stream")
    # Test
    assert resp.status_code == 200
    assert len(resp.json()) == 1


@pytest.mark.asyncio
async def test_get_smallcase_indexes(test_app, f_smallcase_indexes):
    # Given
    id, indexes = await f_smallcase_indexes()
    start_date, end_date = indexes["start_date"], indexes["end_date"]
    # When
    params = {"start_date": start_date, "end_date": end_date}
    resp = await test_app.get(url=f"/smallcases/{id}/indexes", params=params)
    # Test
    assert resp.status_code == 200
    assert len(resp.json()) == len(indexes["indexes"])
