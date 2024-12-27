from pydantic import BaseModel, UUID4
from enum import StrEnum


class Manufacturer(BaseModel):
    id: UUID4
    name: str
    country: str


class Color(StrEnum):
    blue = "blue"
    black = "black"
    white = "white"


class CarIN(BaseModel):
    name: str
    color: Color
    manufacturer_id: UUID4
    details: str | None = None


class CarOUT(BaseModel):
    id: UUID4
    name: str
    color: Color
    manufacturer: Manufacturer


class CarDetails(CarOUT):
    details: str | None = None
