import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_delete_car_204(xclient: AsyncClient):
    response = await xclient.delete("/cars/4")
    assert response.status_code == 204, response.text
    assert response.content == b""


@pytest.mark.asyncio
async def test_delete_car_404(xclient: AsyncClient):
    response = await xclient.delete("/cars/4")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Car not found"}


@pytest.mark.asyncio
async def test_delete_car_422(xclient: AsyncClient):
    response = await xclient.delete("/cars/one")
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
