# tests/test_admin.py
import os
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db
from app.models import Drop
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

client = TestClient(app)
ADMIN_KEY = os.getenv("ADMIN_KEY", "dropspot_admin_2025")


def test_admin_crud_flow(db_session: Session = None):
    payload = {
        "title": "Admin Test Drop",
        "description": "Drop created via test",
        "stock": 5,
        "claim_window_start": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        "claim_window_end": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
    }

    # 1️⃣ Create drop
    response = client.post(
        "/admin/drops",
        headers={"X-Admin-Key": ADMIN_KEY},
        json=payload,
    )
    assert response.status_code == 200
    created_drop = response.json()
    drop_id = created_drop["id"]

    # 2️⃣ List drops
    response = client.get("/admin/drops", headers={"X-Admin-Key": ADMIN_KEY})
    assert response.status_code == 200
    assert any(d["id"] == drop_id for d in response.json())

    # 3️⃣ Update drop
    updated_payload = payload | {"title": "Updated Title"}
    response = client.put(
        f"/admin/drops/{drop_id}",
        headers={"X-Admin-Key": ADMIN_KEY},
        json=updated_payload,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

    # 4️⃣ Delete drop
    response = client.delete(
        f"/admin/drops/{drop_id}",
        headers={"X-Admin-Key": ADMIN_KEY},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Drop deleted successfully"
