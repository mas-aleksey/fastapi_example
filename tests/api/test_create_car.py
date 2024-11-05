import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_car_201(xclient: AsyncClient):
    payload = {"name": "lamba", "color": "black"}
    response = await xclient.post("/cars/", json=payload)
    assert response.status_code == 201, response.text
    assert response.json() == {"id": 4, "name": "lamba", "color": "black",  "details": None}


@pytest.mark.asyncio
async def test_create_car_422_color(xclient: AsyncClient):
    payload = {"name": "lamba", "color": "pink"}
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
    payload = {"color": "blue"}
    response = await xclient.post("/cars/", json=payload)
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "input": {"color": "blue"},
                "loc": ["body", "name"],
                "msg": "Field required",
                "type": "missing"
            }
        ]
    }
