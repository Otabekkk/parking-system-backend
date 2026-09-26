from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class VehicleType(str, Enum):
    CAR = 'CAR'
    MOTORCYCLE = 'MOTORCYCLE'
    TRUCK = 'TRUCK'


class VehicleBase(BaseModel):
    license_plate: str = Field(..., description = 'Номер авто', min_length = 1, max_length = 20)
    vehicle_type: VehicleType = Field(..., description = 'Тип авто')
    owner_name: str = Field(..., description = 'Имя владельца', min_length = 2, max_length = 100)

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    license_plate: Optional[str] = Field(None, min_length = 1, max_length = 20)
    vehicle_type: Optional[VehicleType] = None
    owner_name: Optional[str] = Field(None, min_length = 2, max_length = 100)

class VehicleResponse(VehicleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True