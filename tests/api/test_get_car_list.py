import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_car_list_200(xclient: AsyncClient):
    response = await xclient.get("/cars/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"id": 1, "color": "blue", "name": "BMW",  "details": None},
        {"id": 2, "color": "blue", "name": "Mercedes",  "details": None},
        {"id": 3, "color": "white", "name": "Audi", "details": "awesome car"}
    ]
