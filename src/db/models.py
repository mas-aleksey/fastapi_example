from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class BaseModel(DeclarativeBase):
    id = Column(UUID, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class ManufacturerModel(BaseModel):
    """Модель производителя"""

    __tablename__ = "manufacturer"
    name = Column(String(255), nullable=False, unique=True)
    country = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"Manufacturer({self.id=}, {self.name=}, {self.country=})"


class CarModel(BaseModel):
    """Модель машины"""

    __tablename__ = "car"
    model = Column(String(50), nullable=False)
    color = Column(String(50), nullable=False)
    details = Column(String(255), nullable=True)
    manufacturer_id = Column(ForeignKey(ManufacturerModel.id), nullable=False)

    manufacturer = relationship(ManufacturerModel, backref="cars")

    def __repr__(self) -> str:
        return f"Car({self.id=}, {self.model=}, {self.color=} {self.manufacturer_id=})"
