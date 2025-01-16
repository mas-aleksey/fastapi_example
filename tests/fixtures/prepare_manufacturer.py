from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import ManufacturerModel


@pytest.fixture
def manufacturer_id() -> UUID:
    return uuid4()


@pytest.fixture
def manufacturer(manufacturer_id: UUID) -> ManufacturerModel:
    return ManufacturerModel(
        id=manufacturer_id,
        name="Audi",
        country="Germany",
    )


@pytest_asyncio.fixture
async def prepare_manufacturer(car_db: DatabaseConnector, manufacturer: ManufacturerModel) -> None:
    async with car_db.session_maker(expire_on_commit=False) as session:
        session.add(manufacturer)
        await session.commit()
