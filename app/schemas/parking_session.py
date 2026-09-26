from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from .vehicle import VehicleResponse
from .parking_spot import ParkingSpotResponse

class ParkingSessionBase(BaseModel):
    vehicle_id: int = Field(..., description = 'Id авто')
    parking_spot_id: int = Field(..., description = 'Id парковочного места')

class ParkingSessionCreate(ParkingSessionBase):
    pass

class ParkingSessionResponse(ParkingSessionBase):
    id: int
    entry_time: datetime
    exit_time: Optional[datetime] = None
    cost: Optional[float] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ParkingSessionDetailResponse(ParkingSessionResponse):
    vehicle: VehicleResponse
    parking_spot: ParkingSpotResponse