import logging

from fastapi import HTTPException

from schemas.cars import Car, CarIN

logger = logging.getLogger("car_router")


class CarController:

    def __init__(self, car_db: dict[int, Car]) -> None:
        self.car_db = car_db

    def get_car_list(self) -> list[Car]:
        logger.info("Car list requested")
        return list(self.car_db.values())

    def get_car(self, car_id) -> Car:
        if car_id == 0:
            raise ValueError("Cannot get car with id 0")
        if car_id not in self.car_db:
            raise HTTPException(status_code=404, detail="Car not found")
        return self.car_db.get(car_id)

    def create_car(self, car_in: CarIN) -> Car:
        next_id = max(self.car_db.keys()) + 1
        car = Car(id=next_id, **car_in.model_dump())
        self.car_db[car.id] = car
        return car

    def delete_car(self, car_id) -> None:
        if car_id not in self.car_db:
            raise HTTPException(status_code=404, detail="Car not found")
        self.car_db.pop(car_id)


controller: CarController | None = None


def get_car_controller() -> CarController:
    assert controller is not None, "Car controller not initialized"
    return controller
