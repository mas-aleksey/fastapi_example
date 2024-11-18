from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient

from app import app


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest_asyncio.fixture
async def xclient(client) -> AsyncClient:
    async with AsyncClient(app=app, base_url=client.base_url) as cli:
        yield cli
