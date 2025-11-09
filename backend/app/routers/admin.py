# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import get_db
import os

router = APIRouter(prefix="/admin", tags=["Admin"])

ADMIN_KEY = os.getenv("ADMIN_KEY", "default_admin_key")


def verify_admin_key(x_admin_key: str = Header(...)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin key"
        )


@router.post("/drops", dependencies=[Depends(verify_admin_key)], response_model=schemas.DropOut)
def create_drop(drop: schemas.DropCreate, db: Session = Depends(get_db)):
    new_drop = models.Drop(**drop.dict())
    db.add(new_drop)
    db.commit()
    db.refresh(new_drop)
    return new_drop


@router.put("/drops/{drop_id}", dependencies=[Depends(verify_admin_key)], response_model=schemas.DropOut)
def update_drop(drop_id: int, drop: schemas.DropCreate, db: Session = Depends(get_db)):
    db_drop = db.query(models.Drop).filter(models.Drop.id == drop_id).first()
    if not db_drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    for key, value in drop.dict().items():
        setattr(db_drop, key, value)

    db.commit()
    db.refresh(db_drop)
    return db_drop


@router.delete("/drops/{drop_id}", dependencies=[Depends(verify_admin_key)])
def delete_drop(drop_id: int, db: Session = Depends(get_db)):
    db_drop = db.query(models.Drop).filter(models.Drop.id == drop_id).first()
    if not db_drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    db.delete(db_drop)
    db.commit()
    return {"message": "Drop deleted successfully"}


@router.get("/drops", dependencies=[Depends(verify_admin_key)], response_model=list[schemas.DropOut])
def list_drops(db: Session = Depends(get_db)):
    return db.query(models.Drop).all()
