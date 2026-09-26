from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class VehicleType(str, enum.Enum):
    CAR = 'CAR'
    MOTORCYCLE = 'MOTORCYCLE'
    TRUCK = 'TRUCK'


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key = True, index = True)
    license_plate = Column(String, unique = True, nullable = False, index = True)
    vehicle_type = Column(Enum(VehicleType), nullable = False)
    owner_name = Column(String, nullable = False)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())