import logging

from fastapi import APIRouter, status, Depends

from controllers.car_controller import get_car_controller, CarController
from schemas.cars import Car, CarIN


router = APIRouter()
logger = logging.getLogger("car_router")


@router.get("/", response_model=list[Car])
async def get_car_list(
    controller: CarController = Depends(get_car_controller)
) -> list[Car]:
    return controller.get_car_list()


@router.get("/{car_id}", response_model=Car)
async def get_car(
    car_id: int,
    controller: CarController = Depends(get_car_controller)
) -> Car:
    return controller.get_car(car_id)


@router.post("/", response_model=Car, status_code=status.HTTP_201_CREATED)
async def create_car(
    car_in: CarIN,
    controller: CarController = Depends(get_car_controller)
) -> Car:
    return controller.create_car(car_in)


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
    car_id: int,
    controller: CarController = Depends(get_car_controller)
) -> None:
    controller.delete_car(car_id)
