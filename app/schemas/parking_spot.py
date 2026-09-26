from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class SpotType(str, Enum):
    CAR = 'CAR'
    MOTORCYCLE = 'MOTORCYCLE'
    TRUCK = 'TRUCK'

class ParkingSpotBase(BaseModel):
    spot_number: str = Field(..., description = 'Номер парковочного места', min_length = 1, max_length = 10)
    spot_type: SpotType = Field(..., description = 'Тип парковочного места')

class ParkingSpotCreate(ParkingSpotBase):
    pass

class ParkingSpotUpdate(BaseModel):
    spot_number: Optional[str] = Field(None, min_length = 1, max_length = 10)
    spot_type: Optional[SpotType] = None

class ParkingSpotResponse(ParkingSpotBase):
    id: int
    is_occupied: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True