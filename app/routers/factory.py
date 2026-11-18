from typing import List, Type

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db


def crud_router(
    prefix: str,
    tags: list,
    service_cls: Type,
    create_schema,
    update_schema,
    out_schema,
):
    router = APIRouter(prefix=prefix, tags=tags)

    @router.get("", response_model=List[out_schema])
    def list_items(db: Session = Depends(get_db)):
        return service_cls(db).list()

    @router.get("/{item_id}", response_model=out_schema)
    def get_item(item_id: int, db: Session = Depends(get_db)):
        return service_cls(db).get(item_id)

    @router.post("", response_model=out_schema, status_code=201)
    def create_item(payload: create_schema, db: Session = Depends(get_db)):
        return service_cls(db).create(payload)

    @router.put("/{item_id}", response_model=out_schema)
    def update_item(item_id: int, payload: update_schema, db: Session = Depends(get_db)):
        return service_cls(db).update(item_id, payload)

    @router.delete("/{item_id}")
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        return service_cls(db).delete(item_id)

    return router