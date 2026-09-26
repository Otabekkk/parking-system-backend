from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from  app.database import Base
import enum

class SpotType(str, enum.Enum):
    CAR = 'CAR'
    MOTORCYCLE = 'MOTORCYCLE'
    TRUCK = 'TRUCK'

class ParkingSpot(Base):
    __tablename__ = 'parking_spots'

    id = Column(Integer, primary_key = True, index = True)
    spot_number = Column(String, unique = True, nullable = False, index = True)
    spot_type = Column(Enum(SpotType), nullable = False)
    is_occupied = Column(Boolean, default = False, nullable = False)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())