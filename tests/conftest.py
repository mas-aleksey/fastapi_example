import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app import app


@pytest.fixture(scope="session")
def base_url() -> str:
    return "http://127.0.0.1:8010"


@pytest_asyncio.fixture
async def xclient(base_url: str) -> AsyncClient:
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(base_url=base_url, transport=transport) as cli:
        yield cli


@pytest_asyncio.fixture
async def xclient_debug(base_url: str) -> AsyncClient:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(base_url=base_url, transport=transport) as cli:
        yield cli
