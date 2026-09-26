from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ParkingSession(Base):
    __tablename__ = 'parking_sessions'

    id = Column(Integer, primary_key = True, index = True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable = False)
    parking_spot_id = Column(Integer, ForeignKey('parking_spots.id'), nullable = False)
    entry_time = Column(DateTime(timezone = True), server_default = func.now())
    exit_time = Column(DateTime(timezone = True), nullable = True)
    cost = Column(Float, nullable = True)
    is_active = Column(Boolean, default = True, nullable = False)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())

    # Relationships
    vehicle = relationship('Vehicle', backref = 'parking_sessions')
    parking_spot = relationship('ParkingSpot', backref = 'parking_sessions')