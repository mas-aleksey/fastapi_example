import pytest
import pytest_asyncio
from httpx import AsyncClient

import controllers.car_controller as car_module
from app import app
from models.db import CARS
from schemas.cars import Car


@pytest.fixture(autouse=True)
def car_controller() -> car_module.CarController:
    car_module.controller = car_module.CarController(CARS.copy())
    yield car_module.controller


@pytest.fixture
def car_db(car_controller: car_module.CarController) -> dict[int, Car]:
    return car_controller.car_db


@pytest_asyncio.fixture
async def xclient() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8010") as cli:
        yield cli
