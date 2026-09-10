import secrets
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import users as users_repository
from app.service.tax_id import generate_tax_id
from app.schemas import AuthResponse, UserLoginRequest, UserRegistrationRequest, UserResponse
from app.security import hash_password, verify_password

# Service functions for user management, including registration and login
async def create_user(db: AsyncSession, payload: UserRegistrationRequest) -> UserResponse:
    if await users_repository.get_user_by_full_name(db, payload.full_name):
        raise HTTPException(
            status_code=409,
            detail="A user with this full name already exists"
        )

    if await users_repository.get_user_by_phone(db, payload.phone):
        raise HTTPException(
            status_code=409, 
            detail="A user with this phone already exists"
        )
    
    if await users_repository.get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists",
        )
    tax_id = await generate_tax_id(db, payload.birth_date, payload.gender)
    try:
        user = await users_repository.create_user(
            db,
            payload,
            hash_password(payload.password),
            tax_id,
        )
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A user with this phone or email already exists",
        )
    await db.commit()
    await db.refresh(user)
    return UserResponse.model_validate(user)

# Service function for user login, verifying credentials and generating an access token
async def login_user(db: AsyncSession, payload: UserLoginRequest) -> AuthResponse:
    user = await users_repository.get_user_by_phone(db, payload.phone)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid phone number or password")

    user.access_token = secrets.token_urlsafe(32)
    await db.commit()
    await db.refresh(user)
    return AuthResponse(access_token=user.access_token, user=UserResponse.model_validate(user))
    
