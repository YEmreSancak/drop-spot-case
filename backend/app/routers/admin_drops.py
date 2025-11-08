from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
from app.auth import get_current_admin_user

router = APIRouter(prefix="/admin/drops", tags=["Admin Drops"])


@router.post("", response_model=schemas.DropOut)
def create_drop(payload: schemas.DropCreate,
                db: Session = Depends(get_db),
                admin=Depends(get_current_admin_user)):
    drop = models.Drop(**payload.dict())
    db.add(drop)
    db.commit()
    db.refresh(drop)
    return drop


@router.put("/{drop_id}", response_model=schemas.DropOut)
def update_drop(drop_id: int,
                payload: schemas.DropUpdate,
                db: Session = Depends(get_db),
                admin=Depends(get_current_admin_user)):
    drop = db.query(models.Drop).filter(models.Drop.id == drop_id).first()
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(drop, key, value)

    db.commit()
    db.refresh(drop)
    return drop


@router.delete("/{drop_id}", status_code=204)
def delete_drop(drop_id: int,
                db: Session = Depends(get_db),
                admin=Depends(get_current_admin_user)):
    drop = db.query(models.Drop).filter(models.Drop.id == drop_id).first()
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")
    db.delete(drop)
    db.commit()
    return
