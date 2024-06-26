import pytest


@pytest.fixture(scope="function")
def f_smallcase_payload(faker):
    return {
        "id": faker.word(),
        "name": faker.word(),
        "slug": faker.word(),
        "description": faker.word(),
        "volatility": "Low Volatility",
        "contains_etf": faker.pybool(),
        "contains_stock": faker.pybool(),
        "constituent_count": faker.random_int(min=1, max=20),
        "benchmark": {
            "id": faker.word(),
            "index": faker.word(),
            "details": faker.word(),
        },
        "growth_since_launch": {
            "cagr": faker.pyfloat(),
            "returns": faker.pyfloat(),
            "duration": faker.word(),
        },
        "methodologies": [{"key": faker.word(), "details": faker.word()}],
        "launch_date": "2020-01-01",
        "inception_date": "2020-01-01",
        "last_rebalance_date": "2020-01-01",
        "next_rebalance_date": "2020-01-01",
        "investment_strategies": [faker.word()],
        "rebalance_frequency": "monthly",
    }


@pytest.fixture(scope="function")
def f_smallcase(test_app, f_smallcase_payload):
    async def _f_smallcase_base():
        smallcase = f_smallcase_payload
        resp = await test_app.post(url="/smallcases", json=smallcase)
        assert resp.status_code == 201
        return smallcase["id"]

    return _f_smallcase_base


@pytest.fixture(scope="function")
def f_smallcase_constituents_payload(faker):
    return {
        "start_date": "2020-01-01",
        "end_date": "2020-03-30",
        "constituents": [
            {
                "smallcase_name": faker.word(),
                "original_weightage": faker.pyfloat(),
                "kelly_weightage": faker.pyfloat(),
                "standard_deviation": faker.pyfloat(),
            },
            {
                "smallcase_name": faker.word(),
                "original_weightage": faker.pyfloat(),
                "kelly_weightage": faker.pyfloat(),
                "standard_deviation": faker.pyfloat(),
            },
        ],
    }


@pytest.fixture(scope="function")
def f_smallcase_constituents(
    test_app, f_smallcase_payload, f_smallcase_constituents_payload
):
    async def _f_smallcase_constituents():
        smallcase = f_smallcase_payload
        id = smallcase["id"]
        resp = await test_app.post(url="/smallcases", json=smallcase)
        assert resp.status_code == 201

        url = f"/smallcases/{id}/constituents"
        constituents = f_smallcase_constituents_payload
        resp = await test_app.post(url=url, json=constituents)
        assert resp.status_code == 201
        return id, constituents

    return _f_smallcase_constituents


@pytest.fixture(scope="function")
def f_smallcase_indexes_payload(faker):
    return {
        "start_date": "2020-01-01",
        "end_date": "2020-01-03",
        "indexes": {
            "2020-01-01": {
                "kelly": faker.pyfloat(),
                "smallcase": faker.pyfloat(),
                "benchmark": faker.pyfloat(),
            },
            "2020-01-02": {
                "kelly": faker.pyfloat(),
                "smallcase": faker.pyfloat(),
                "benchmark": faker.pyfloat(),
            },
            "2020-01-03": {
                "kelly": faker.pyfloat(),
                "smallcase": faker.pyfloat(),
                "benchmark": faker.pyfloat(),
            },
        },
    }


@pytest.fixture(scope="function")
def f_smallcase_indexes(test_app, f_smallcase_payload, f_smallcase_indexes_payload):
    async def _f_smallcase_indexes():
        smallcase = f_smallcase_payload
        id = smallcase["id"]
        resp = await test_app.post(url="/smallcases", json=smallcase)
        assert resp.status_code == 201

        url = f"/smallcases/{id}/indexes"
        indexes = f_smallcase_indexes_payload
        params = {"date": indexes["start_date"]}
        resp = await test_app.post(url=url, params=params, json=indexes)
        assert resp.status_code == 201
        return id, indexes

    return _f_smallcase_indexes
