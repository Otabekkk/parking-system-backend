from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from typing import List, Optional

def get_vehicles(db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
    """
      Получить список всех автомобилей с пагинацией

      Args:
          db: Сессия БД
          skip: Сколько записей пропустить (для пагинации)
          limit: Максимум записей вернуть

      Returns:
          Список автомобилей
    """
    return db.query(Vehicle).offset(skip).limit(limit).all()

def get_vehicle(db: Session, vehicle_id: int) -> Optional[Vehicle]:
    """
      Получить автомобиль по ID

      Args:
          db: Сессия БД
          vehicle_id: ID автомобиля

      Returns:
          Автомобиль или None если не найден
    """
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

def create_vehicle(db: Session, vehicle: VehicleCreate) -> Vehicle:
    """
      Создать новый автомобиль

      Args:
          db: Сессия БД
          vehicle: Данные для создания

      Returns:
          Созданный автомобиль
    """
    db_vehicle = Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle

def update_vehicle(db: Session, vehicle_id: int, vehicle: VehicleUpdate) -> Optional[Vehicle]:
    """
      Обновить автомобиль

      Args:
          db: Сессия БД
          vehicle_id: ID автомобиля
          vehicle: Данные для обновления

      Returns:
          Обновленный автомобиль или None если не найден
    """
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if db_vehicle is None:
        return None

    update_data = vehicle.model_dump(exclude_unset = True)

    for key, value in update_data.items():
        setattr(db_vehicle, key, value)

    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle

def delete_vehicle(db: Session, vehicle_id: int) -> bool:
    """
      Удалить автомобиль

      Args:
          db: Сессия БД
          vehicle_id: ID автомобиля

      Returns:
          True если удален, False если не найден
    """
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    
    if db_vehicle is None:
        return False

    db.delete(db_vehicle)
    db.commit()

    return True