import pytest
from httpx import AsyncClient

from db.models import CarModel, ManufacturerModel


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_car")
async def test_get_car_list_200(xclient: AsyncClient, car: CarModel, manufacturer: ManufacturerModel):
    response = await xclient.get("/cars/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "id": str(car.id),
            "name": car.model,
            "color": car.color,
            "manufacturer": {
                "id": str(manufacturer.id),
                "name": manufacturer.name,
                "country": manufacturer.country
            }
        }
    ]
