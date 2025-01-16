import pytest
import pytest_asyncio
from httpx import AsyncClient

import controllers.car_controller as car_module
from app import app

from core.settings import get_settings, Settings
from db.connector import DatabaseConnector

pytest_plugins = [
    "fixtures.car_db",
    "fixtures.prepare_car",
    "fixtures.prepare_manufacturer",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(autouse=True)
def car_controller(car_db: DatabaseConnector) -> car_module.CarController:
    car_module.controller = car_module.CarController(car_db)
    yield car_module.controller


@pytest_asyncio.fixture
async def xclient() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8010") as cli:
        yield cli
