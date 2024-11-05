from pydantic import BaseModel
from enum import StrEnum


class Color(StrEnum):
    blue = "blue"
    black = "black"
    white = "white"


class CarIN(BaseModel):
    name: str
    color: Color
    details: str | None = None


class Car(CarIN):
    id: int
