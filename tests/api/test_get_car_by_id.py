import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "car_id,expected", [
        (1, {"id": 1, "color": "blue", "name": "BMW",  "details": None}),
        (2, {"id": 2, "color": "blue", "name": "Mercedes",  "details": None}),
        (3, {"id": 3, "color": "white", "name": "Audi", "details": "awesome car"})
    ]
)
async def test_get_car_200(xclient: AsyncClient, car_id, expected):
    response = await xclient.get(f"/cars/{car_id}")
    assert response.status_code == 200, response.text
    assert response.json() == expected


@pytest.mark.asyncio
async def test_get_car_404(xclient: AsyncClient):
    response = await xclient.get("/cars/999")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Car not found"}


@pytest.mark.asyncio
async def test_get_car_422(xclient: AsyncClient):
    response = await xclient.get("/cars/one")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "input": "one",
                "loc": ["path", "car_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "type": "int_parsing"
            }
        ]
    }


@pytest.mark.asyncio
async def test_get_car_500(xclient: AsyncClient):
    response = await xclient.get("/cars/0")
    assert response.status_code == 500, response.text
    assert response.json() == {
        'message': 'Failed method GET at URL http://127.0.0.1:8010/cars/0. Exception '"message is ValueError('Cannot delete car with id 0')."
    }
