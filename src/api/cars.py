import logging

from fastapi import APIRouter, status, Depends
from pydantic import UUID4

from controllers.car_controller import get_car_controller, CarController
from schemas.cars import CarOUT, CarIN, CarDetails


router = APIRouter()
logger = logging.getLogger("car_router")


@router.get("/")
async def get_car_list(
    controller: CarController = Depends(get_car_controller)
) -> list[CarOUT]:
    return await controller.get_car_list()


@router.get("/{car_id}")
async def get_car(
    car_id: UUID4,
    controller: CarController = Depends(get_car_controller)
) -> CarDetails:
    return await controller.get_car(car_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_car(
    car_in: CarIN,
    controller: CarController = Depends(get_car_controller)
) -> CarOUT:
    return await controller.create_car(car_in)


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
    car_id: UUID4,
    controller: CarController = Depends(get_car_controller)
) -> None:
    await controller.delete_car(car_id)
