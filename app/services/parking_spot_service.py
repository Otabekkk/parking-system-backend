from sqlalchemy.orm import Session
from app.models.parking_spot import ParkingSpot
from app.schemas.parking_spot import ParkingSpotCreate, ParkingSpotUpdate
from typing import List, Optional

def get_parking_spots(db: Session, skip: int = 0, limit: int = 100) -> List[ParkingSpot]:
    """
    Получить список всех парковочных мест с пагинацией

    Args:
        db: Сессия БД
        skip: Сколько записей пропустить (для пагинации)
        limit: Максимум записей вернуть

    Returns:
        Список парковочных мест
    """
    return db.query(ParkingSpot).offset(skip).limit(limit).all()

def get_parking_spot(db: Session, parking_spot_id: int) -> Optional[ParkingSpot]:
    """
      Получить парковочное место по ID

      Args:
          db: Сессия БД
          parking_spot_id: ID парковочного места

      Returns:
          Парковочное место или None если не найден
    """
    return db.query(ParkingSpot).filter(ParkingSpot.id == parking_spot_id).first()

def create_parking_spot(db: Session, parking_spot: ParkingSpotCreate) -> ParkingSpot:
    """
      Создать новое парковочное место

      Args:
          db: Сессия БД
          parking_spot: Данные для создания

      Returns:
          Созданное парковочное место
    """
    db_parking_spot = ParkingSpot(**parking_spot.model_dump())
    db.add(db_parking_spot)
    db.commit()
    db.refresh(db_parking_spot)

    return db_parking_spot

def update_parking_spot(db: Session, parking_spot_id: int, parking_spot: ParkingSpotUpdate) -> Optional[ParkingSpot]:
    """
      Обновить парковочное место

      Args:
          db: Сессия БД
          parking_spot_id: ID парк. места
          parking_spot: Данные для обновления

      Returns:
          Обновленное парк. место или None если не найдено
    """
    db_parking_spot = db.query(ParkingSpot).filter(ParkingSpot.id == parking_spot_id).first()

    if db_parking_spot is None:
        return None

    update_data = parking_spot.model_dump(exclude_unset = True)

    for key, value in update_data.items():
        setattr(db_parking_spot, key, value)

    db.commit()
    db.refresh(db_parking_spot)

    return db_parking_spot

def delete_parking_spot(db: Session, parking_spot_id: int) -> bool:
    """
      Удалить парковочное место

      Args:
          db: Сессия БД
          parking_spot_id: ID парковочного места

      Returns:
          True если удален, False если не найден
    """
    db_parking_spot = db.query(ParkingSpot).filter(ParkingSpot.id == parking_spot_id).first()

    if db_parking_spot is None:
        return False

    db.delete(db_parking_spot)
    db.commit()

    return True

def get_available_spots(db: Session, spot_type: Optional[str] = None) -> list[ParkingSpot]:
    """
    Получить список свободных парковочных мест

    Args:
      db: Сессия БД
      spot_type: Фильтр по типу места (опционально)

    Returns:
      Список свободных мест
    """

    query = db.query(ParkingSpot).filter(ParkingSpot.is_occupied == False)
    
    if spot_type:
        query = query.filter(ParkingSpot.spot_type == spot_type)
    
    return query.all()