from uuid import uuid4
from unittest.mock import ANY

import pytest
from httpx import AsyncClient

from db.connector import DatabaseConnector
from db.models import CarModel, ManufacturerModel


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_create_car_201(xclient: AsyncClient, car_db: DatabaseConnector, manufacturer: ManufacturerModel):
    payload = {"name": "rs6", "color": "white", "manufacturer_id": str(manufacturer.id)}
    response = await xclient.post("/cars/", json=payload)

    assert response.status_code == 201, response.text
    data = response.json()
    assert data == {
        "id": ANY,
        "name": "rs6",
        "color": "white",
        "manufacturer": {
            "id": str(manufacturer.id),
            "name": manufacturer.name,
            "country": manufacturer.country
        }
    }
    async with car_db.session_maker() as session:
        car_db = await session.get(CarModel, data["id"])
    assert car_db.model == data["name"]
    assert car_db.color == data["color"]
    assert car_db.manufacturer_id == manufacturer.id


@pytest.mark.asyncio
async def test_create_car_422_color(xclient: AsyncClient):
    payload = {"name": "lamba", "color": "pink", "manufacturer_id": str(uuid4())}
    response = await xclient.post("/cars/", json=payload)
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "ctx": {"expected": "'blue', 'black' or 'white'"},
                "input": "pink",
                "loc": ["body", "color"],
                "msg": "Input should be 'blue', 'black' or 'white'",
                "type": "enum"
            }
        ]
    }


@pytest.mark.asyncio
async def test_create_car_422_name(xclient: AsyncClient):
    payload = {"color": "blue", "manufacturer_id": str(uuid4())}
    response = await xclient.post("/cars/", json=payload)
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "input": payload,
                "loc": ["body", "name"],
                "msg": "Field required",
                "type": "missing"
            }
        ]
    }
