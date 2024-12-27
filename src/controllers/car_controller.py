import logging
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db.connector import DatabaseConnector
from db.models import CarModel
from schemas.cars import CarIN, CarDetails, CarOUT, Manufacturer

logger = logging.getLogger("car_router")


class CarController:

    def __init__(self, car_db: DatabaseConnector) -> None:
        self.car_db = car_db

    async def get_car_list(self) -> list[CarOUT]:
        logger.info("Car list requested")
        async with self.car_db.session_maker() as session:
            cursor = await session.execute(
                select(CarModel).options(joinedload(CarModel.manufacturer))
            )
            cars = cursor.scalars().all()
        return [
            CarOUT(
                id=car.id,
                name=car.model,
                color=car.color,
                manufacturer=Manufacturer(
                    id=car.manufacturer.id,
                    name=car.manufacturer.name,
                    country=car.manufacturer.country
                ),
            ) for car in cars
        ]

    async def get_car(self, car_id) -> CarDetails:
        async with self.car_db.session_maker() as session:
            car = await session.get(CarModel, car_id, options=[joinedload(CarModel.manufacturer)])
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        return CarDetails(
            id=car.id,
            name=car.model,
            color=car.color,
            manufacturer=Manufacturer(
                id=car.manufacturer.id,
                name=car.manufacturer.name,
                country=car.manufacturer.country
            ),
            details=car.details
        )

    async def create_car(self, car_in: CarIN) -> CarOUT:
        car_id = uuid.uuid4()
        async with self.car_db.session_maker() as session:
            car = CarModel(
                id=car_id,
                model=car_in.name,
                color=car_in.color,
                manufacturer_id=car_in.manufacturer_id,
                details=car_in.details
            )
            session.add(car)
            await session.commit()
        return await self.get_car(car_id)

    async def delete_car(self, car_id) -> None:
        async with self.car_db.session_maker() as session:
            car = await session.get(CarModel, car_id)
            if not car:
                raise HTTPException(status_code=404, detail="Car not found")
            await session.delete(car)
            await session.commit()
        logger.info(f"Car {car_id} deleted")


controller: CarController | None = None


def get_car_controller() -> CarController:
    assert controller is not None, "Car controller not initialized"
    return controller
