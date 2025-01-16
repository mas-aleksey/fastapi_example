from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from db.connector import DatabaseConnector
from db.models import CarModel


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_car")
async def test_delete_car_204(xclient: AsyncClient,  car_db: DatabaseConnector, car_id: UUID):
    response = await xclient.delete(f"/cars/{car_id}")
    assert response.status_code == 204, response.text
    assert response.content == b""
    async with car_db.session_maker() as session:
        deleted_car = await session.get(CarModel, car_id)
    assert deleted_car is None


@pytest.mark.asyncio
async def test_delete_car_404(xclient: AsyncClient):
    response = await xclient.delete(f"/cars/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Car not found"}


@pytest.mark.asyncio
async def test_delete_car_422(xclient: AsyncClient):
    response = await xclient.delete("/cars/one")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `o` at 1'},
                "input": "one",
                "loc": ["path", "car_id"],
                "msg": "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `o` at 1",
                "type": "uuid_parsing"
            }
        ]
    }
