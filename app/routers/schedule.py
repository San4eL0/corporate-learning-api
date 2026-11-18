from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ScheduleCreate, ScheduleOut, ScheduleUpdate
from app.services import ScheduleService

router = APIRouter(prefix="/schedule", tags=["schedule"])

service_cls = ScheduleService


@router.get("", response_model=List[ScheduleOut])
def list_schedules(db: Session = Depends(get_db)):
    return service_cls(db).list()


@router.get("/in-progress", response_model=List[ScheduleOut])
def schedules_in_progress(db: Session = Depends(get_db)):
    return service_cls(db).in_progress()


@router.get("/{schedule_id}", response_model=ScheduleOut)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    return service_cls(db).get(schedule_id)


@router.post("", response_model=ScheduleOut, status_code=201)
def create_schedule(payload: ScheduleCreate, db: Session = Depends(get_db)):
    return service_cls(db).create(payload)


@router.put("/{schedule_id}", response_model=ScheduleOut)
def update_schedule(
    schedule_id: int, payload: ScheduleUpdate, db: Session = Depends(get_db)
):
    return service_cls(db).update(schedule_id, payload)


@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    return service_cls(db).delete(schedule_id)