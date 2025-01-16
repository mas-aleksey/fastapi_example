from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import CarModel


@pytest.fixture
def car_id() -> UUID:
    return uuid4()


@pytest.fixture
def car(car_id: UUID, manufacturer_id: UUID) -> CarModel:
    return CarModel(
        id=car_id,
        model="rs6",
        color="white",
        manufacturer_id=manufacturer_id,
    )


@pytest_asyncio.fixture
async def prepare_car(car_db: DatabaseConnector, car: CarModel, prepare_manufacturer: None) -> None:
    async with car_db.session_maker(expire_on_commit=False) as session:
        session.add(car)
        await session.commit()
