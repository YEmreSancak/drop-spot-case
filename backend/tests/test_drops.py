from uuid import uuid4
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app
from app.db import SessionLocal
from app import models

client = TestClient(app)


def create_admin_user():
    email = f"admin_{uuid4().hex[:8]}@example.com"
    password = "AdminPass123!"

    # signup
    resp = client.post("/auth/signup", json={"email": email, "password": password})
    assert resp.status_code == 200, resp.text

    # admin flag set
    db = SessionLocal()
    try:
        user = db.query(models.User).filter_by(email=email).first()
        user.is_admin = True
        db.commit()
    finally:
        db.close()

    # login
    login_resp = client.post("/auth/login", json={"email": email, "password": password})
    assert login_resp.status_code == 200, login_resp.text
    token = login_resp.json()["access_token"]
    return email, token


def create_regular_user():
    email = f"user_{uuid4().hex[:8]}@example.com"
    password = "UserPass123!"
    resp = client.post("/auth/signup", json={"email": email, "password": password})
    assert resp.status_code == 200, resp.text

    login_resp = client.post("/auth/login", json={"email": email, "password": password})
    assert login_resp.status_code == 200, login_resp.text
    token = login_resp.json()["access_token"]
    return email, token


def create_active_drop(admin_token: str) -> int:
    now = datetime.now(timezone.utc)
    payload = {
        "name": "Test Drop",
        "description": "Integration test drop",
        "total_quantity": 5,
        "claim_start_at": (now - timedelta(minutes=5)).isoformat(),
        "claim_end_at": (now + timedelta(minutes=30)).isoformat(),
        "is_active": True,
    }

    resp = client.post(
        "/admin/drops",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["id"]


def test_waitlist_and_claim_idempotent_flow():
    # 1) Admin + drop oluştur
    _, admin_token = create_admin_user()
    drop_id = create_active_drop(admin_token)

    # 2) Normal kullanıcı oluştur
    _, user_token = create_regular_user()

    # 3) Waitlist'e iki kez join (idempotent)
    join_resp1 = client.post(
        f"/drops/{drop_id}/join",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    join_resp2 = client.post(
        f"/drops/{drop_id}/join",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert join_resp1.status_code == 200
    assert join_resp2.status_code == 200
    assert join_resp1.json()["status"] == "joined"
    assert join_resp2.json()["status"] == "joined"

    # DB'de tek kayıt olmalı
    db = SessionLocal()
    try:
        entries = (
            db.query(models.WaitlistEntry)
            .filter(
                models.WaitlistEntry.drop_id == drop_id,
            )
            .all()
        )
        assert len(entries) == 1
    finally:
        db.close()

    # 4) Waitlist'ten iki kez leave (idempotent)
    leave_resp1 = client.post(
        f"/drops/{drop_id}/leave",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    leave_resp2 = client.post(
        f"/drops/{drop_id}/leave",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert leave_resp1.status_code == 200
    assert leave_resp2.status_code == 200
    assert leave_resp1.json()["status"] == "left"
    assert leave_resp2.json()["status"] == "left"

    # 5) Tekrar join et ve claim akışını test et
    rejoin_resp = client.post(
        f"/drops/{drop_id}/join",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert rejoin_resp.status_code == 200

    claim_resp1 = client.post(
        f"/drops/{drop_id}/claim",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert claim_resp1.status_code == 200, claim_resp1.text
    claim_code_1 = claim_resp1.json()["claim_code"]

    # Tekrar claim denemesi aynı kodu döndürmeli (idempotent)
    claim_resp2 = client.post(
        f"/drops/{drop_id}/claim",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert claim_resp2.status_code == 200, claim_resp2.text
    claim_code_2 = claim_resp2.json()["claim_code"]

    assert claim_code_1 == claim_code_2

    # DB'de tek claim olmalı
    db = SessionLocal()
    try:
        claims = (
            db.query(models.Claim)
            .filter(
                models.Claim.drop_id == drop_id,
            )
            .all()
        )
        assert len(claims) == 1
    finally:
        db.close()
