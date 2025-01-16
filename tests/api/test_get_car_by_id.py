from uuid import uuid4

import pytest
from httpx import AsyncClient

from db.models import CarModel, ManufacturerModel


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_car")
async def test_get_car_200(xclient: AsyncClient, car: CarModel, manufacturer: ManufacturerModel):
    response = await xclient.get(f"/cars/{car.id}")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": str(car.id),
        "name": car.model,
        "color": car.color,
        "details": car.details,
        "manufacturer": {
            "id": str(manufacturer.id),
            "name": manufacturer.name,
            "country": manufacturer.country
        }
    }


@pytest.mark.asyncio
async def test_get_car_404(xclient: AsyncClient):
    response = await xclient.get(f"/cars/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Car not found"}


@pytest.mark.asyncio
async def test_get_car_422(xclient: AsyncClient):
    response = await xclient.get("/cars/one")
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
