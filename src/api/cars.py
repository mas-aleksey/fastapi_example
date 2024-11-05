import logging

from fastapi import APIRouter, HTTPException, status
from schemas.cars import Car, CarIN, Color


router = APIRouter()
logger = logging.getLogger("car_router")


CARS = {
    1: Car(id=1, name="BMW", color=Color.blue),
    2: Car(id=2, name="Mercedes", color=Color.blue),
    3: Car(id=3, name="Audi", color=Color.white, details="awesome car"),
}


@router.get("/", response_model=list[Car])
async def get_car_list() -> list[Car]:
    logger.info("Car list requested")
    return list(CARS.values())


@router.get("/{car_id}", response_model=Car)
async def get_car(car_id: int) -> Car:
    if car_id == 0:
        raise ValueError("Cannot delete car with id 0")
    if car_id not in CARS:
        raise HTTPException(status_code=404, detail="Car not found")
    return CARS.get(car_id)


@router.post("/", response_model=Car, status_code=status.HTTP_201_CREATED)
async def create_car(car: CarIN) -> Car:
    next_id = max(CARS.keys()) + 1
    car = Car(id=next_id, **car.model_dump())
    CARS[car.id] = car
    return car


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: int) -> None:
    if car_id not in CARS:
        raise HTTPException(status_code=404, detail="Car not found")
    CARS.pop(car_id)
