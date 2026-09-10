from sqlalchemy import select
from app.models import User
from app.security import verify_password


async def test_register_user_creates_hashed_password(
    client,
    db_session,
) -> None:
    payload = {
        "full_name": "Петренко Іван Олексійович",
        "phone": "+380501234567",
        "password": "StrongPassword123",
        "birth_date": "2000-01-01",
        "email": "ivan@example.com",
        "gender": "male",
    }
    
    response = await client.post("/api/v1/users", json=payload)
    
    assert response.status_code == 200
    
    body = response.json()
    assert body["phone"] == "+380501234567"
    assert body["email"] == "ivan@example.com"
    assert "password" not in body
    assert "password_hash" not in body
    
    user = await db_session.scalar(
        select(User).where(User.phone == "+380501234567")
    )
    
    assert user is not None
    assert user.password_hash != payload["password"]
    assert verify_password(payload["password"], user.password_hash)


async def test_login_returns_access_token(client) -> None:
    registration_payload = {
        "full_name": "Іван Петренко",
        "phone": "+380501234567",
        "password": "StrongPassword123",
        "birth_date": "2000-01-01",
        "email": "ivan@example.com",
        "gender": "male",
    }

    await client.post("/api/v1/users", json=registration_payload)

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "phone": "+380501234567",
            "password": "StrongPassword123",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["user"]["phone"] == "+380501234567"