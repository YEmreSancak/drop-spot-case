from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
import uuid

from app.db import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/drops", tags=["Drops"])


@router.get("", response_model=list[schemas.DropOut])
def list_active_drops(db: Session = Depends(get_db)):
    drops = (
        db.query(models.Drop)
        .filter(models.Drop.is_active == True)
        .order_by(models.Drop.claim_start_at.asc())
        .all()
    )
    return drops


@router.post("/{drop_id}/join")
def join_waitlist(drop_id: int,
                  db: Session = Depends(get_db),
                  current_user=Depends(get_current_user)):
    drop = db.query(models.Drop).filter(models.Drop.id == drop_id, models.Drop.is_active == True).first()
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    entry = models.WaitlistEntry(user_id=current_user.id, drop_id=drop_id)

    try:
        db.add(entry)
        db.commit()
    except IntegrityError:
        db.rollback()
        # zaten waitlist'te → idempotent
    return {"status": "joined"}


@router.post("/{drop_id}/leave")
def leave_waitlist(drop_id: int,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_user)):
    entry = (
        db.query(models.WaitlistEntry)
        .filter(
            models.WaitlistEntry.user_id == current_user.id,
            models.WaitlistEntry.drop_id == drop_id,
        )
        .first()
    )
    if entry:
        db.delete(entry)
        db.commit()
    # yoksa da 200 → idempotent
    return {"status": "left"}


@router.post("/{drop_id}/claim")
def claim_drop(drop_id: int,
               db: Session = Depends(get_db),
               current_user=Depends(get_current_user)):
    now = datetime.now(timezone.utc)

    drop = db.query(models.Drop).filter(models.Drop.id == drop_id).first()
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    if not (drop.claim_start_at <= now <= drop.claim_end_at):
        raise HTTPException(status_code=400, detail="Claim window is not active")

    # Kullanıcı waitlist'te mi?
    in_waitlist = (
        db.query(models.WaitlistEntry)
        .filter(
            models.WaitlistEntry.user_id == current_user.id,
            models.WaitlistEntry.drop_id == drop_id,
        )
        .first()
    )
    if not in_waitlist:
        raise HTTPException(status_code=403, detail="Not eligible for this drop")

    # Idempotent claim: varsa aynı kodu döndür
    existing_claim = (
        db.query(models.Claim)
        .filter(
            models.Claim.user_id == current_user.id,
            models.Claim.drop_id == drop_id,
        )
        .first()
    )
    if existing_claim:
        return {"claim_code": existing_claim.claim_code}

    # Toplam claim sayısını kontrol et
    total_claims = db.query(models.Claim).filter(models.Claim.drop_id == drop_id).count()
    if total_claims >= drop.total_quantity:
        raise HTTPException(status_code=400, detail="No more claimable items")

    # Yeni claim oluştur
    claim_code = f"{drop_id}-{uuid.uuid4().hex[:10]}"

    new_claim = models.Claim(
        user_id=current_user.id,
        drop_id=drop_id,
        claim_code=claim_code,
    )
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)

    return {"claim_code": new_claim.claim_code}
