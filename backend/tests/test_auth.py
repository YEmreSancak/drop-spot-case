from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_signup_login_and_me_flow():
    # her koşuda benzersiz bir kullanıcı üretelim
    unique_email = f"testuser_{uuid4().hex[:8]}@example.com"
    password = "TestPassword123!"

    # 1) Signup
    signup_response = client.post(
        "/auth/signup",
        json={"email": unique_email, "password": password},
    )

    assert signup_response.status_code == 200, signup_response.text
    signup_data = signup_response.json()

    assert signup_data["email"] == unique_email
    assert "id" in signup_data

    # 2) Login
    login_response = client.post(
        "/auth/login",
        json={"email": unique_email, "password": password},
    )

    assert login_response.status_code == 200, login_response.text
    login_data = login_response.json()

    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"

    access_token = login_data["access_token"]

    # 3) /auth/me ile token'ı doğrula
    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert me_response.status_code == 200, me_response.text
    me_data = me_response.json()

    assert me_data["email"] == unique_email
    assert "id" in me_data
