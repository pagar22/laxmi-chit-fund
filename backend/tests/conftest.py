import asyncio

import pytest
import pytest_asyncio
from app.internal.config import IS_EMULATOR_CONNECTED

# from app.internal.firebase import log
from app.main import app
from faker import Faker
from firebase_admin import firestore_async
from httpx import ASGITransport, AsyncClient

from .factories import *


@pytest_asyncio.fixture(scope="session", autouse=True)
def confirm_environment():
    if not IS_EMULATOR_CONNECTED:
        pytest.fail("🚨 FATAL: Cannot run tests without an emulator connected.")


@pytest_asyncio.fixture(scope="session")
def faker() -> Faker:
    faker = Faker("en_GB")
    faker.random.seed()
    return faker


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def test_app():
    transport = ASGITransport(app)
    async with AsyncClient(
        transport=transport, base_url="http://test", follow_redirects=True
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def cleanup():
    yield
    # log.info("🫧 Cleaning Firestore emulator...")
    db = firestore_async.client()
    db_collections = ["smallcases", "tickers"]
    for collection in db_collections:
        docs = db.collection(collection).stream()
        async for doc in docs:
            await doc.reference.delete()
