from sqlalchemy.orm import Session

from app.models.parking_session import ParkingSession
from app.models.parking_spot import ParkingSpot
from app.models.vehicle import Vehicle

from app.schemas.parking_session import ParkingSessionCreate

from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException

TARIFFS = {
    "CAR": 100,
    "MOTORCYCLE": 50,
    "TRUCK": 150
}

def get_parking_sessions(db: Session, skip: int = 0, limit: int = 100) -> list[ParkingSession]:
    """Получить список всех сессий"""
    return db.query(ParkingSession).offset(skip).limit(limit).all()

def get_parking_session(db: Session, session_id: int) -> Optional[ParkingSession]:
    """Получить сессию по ID"""
    return db.query(ParkingSession).filter(ParkingSession.id == session_id).first()

def get_active_sessions(db: Session) -> List[ParkingSession]:
    """Получить список активных сессий"""
    return db.query(ParkingSession).filter(ParkingSession.is_active == True).all()

def check_in(db: Session, session_data: ParkingSessionCreate) -> ParkingSession:
    """
    Въезд автомобиля на парковку

    Проверки:
    1. Автомобиль существует
    2. Парковочное место существует
    3. Типы совместимы (CAR может на место CAR)
    4. Место свободно
    5. Автомобиль не находится уже на парковке

    Args:
      db: Сессия БД
      session_data: Данные для создания сессии

    Returns:
      Созданная сессия

    Raises:
      HTTPException: Если проверки не прошли
    """
    # Auto exists
    vehicle = db.query(Vehicle).filter(Vehicle.id == session_data.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code = 404, detail = f'Автомобиль с ID {session_data.vehicle_id} не найден')

    # Parking place exists
    parking_spot = db.query(ParkingSpot).filter(ParkingSpot.id == session_data.parking_spot_id).first()
    if not parking_spot:
      raise HTTPException(status_code=404, detail=f"Парковочное место с ID {session_data.parking_spot_id} не найдено")

    # Auto type == parking spot type
    if vehicle.vehicle_type.value != parking_spot.spot_type.value:
        raise HTTPException(
          status_code=400,
          detail=f"Несовместимые типы: автомобиль {vehicle.vehicle_type.value} не может припарковаться на месте для {parking_spot.spot_type.value}"
        )

    # Spot is available
    if parking_spot.is_occupied:
        raise HTTPException(status_code=400, detail=f"Парковочное место {parking_spot.spot_number} уже занято")

    # Auto has not another spot
    active_session = db.query(ParkingSession).filter(
        ParkingSession.vehicle_id == session_data.vehicle_id,
            ParkingSession.is_active == True
    ).first()

    if active_session:
        raise HTTPException(
            status_code=400,
            detail=f"Автомобиль {vehicle.license_plate} уже находится на парковке (место {active_session.parking_spot_id})"
        )

    db_session = ParkingSession(**session_data.model_dump())
    db.add(db_session)

    parking_spot.is_occupied = True

    db.commit()
    db.refresh(db_session)

    return db_session

def check_out(db: Session, session_id: int) -> ParkingSession:
    """
    Выезд автомобиля с парковки и расчет стоимости

    Args:
        db: Сессия БД
        session_id: ID сессии

    Returns:
        Обновленная сессия с рассчитанной стоимостью

    Raises:
        HTTPException: Если сессия не найдена или уже завершена
    """
    session = db.query(ParkingSession).filter(ParkingSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Сессия с ID {session_id} не найдена")

    if not session.is_active:
        raise HTTPException(status_code=400, detail="Сессия уже завершена")

    session.exit_time = datetime.now()

    duration = session.exit_time - session.entry_time
    hours = duration.total_seconds() / 3600

    import math
    hours_rounded = math.ceil(hours) if hours > 0 else 0

    vehicle = db.query(Vehicle).filter(Vehicle.id == session.vehicle_id).first()
    tariff = TARIFFS[vehicle.vehicle_type.value]

    session.cost = hours_rounded * tariff

    session.is_active = False

    parking_spot = db.query(ParkingSpot).filter(ParkingSpot.id == session.parking_spot_id).first()
    parking_spot.is_occupied = False

    db.commit()
    db.refresh(session)
    
    return session