
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import UserRegistrationRequest


# Function to retrieve a user by their full name
async def get_user_by_full_name(db: AsyncSession, full_name: str) -> User | None:
    query = select(User).where(User.full_name == full_name)
    return await db.scalar(query)

# Function to retrieve a user by their phone number
async def get_user_by_phone(db: AsyncSession, phone: str) -> User | None:
    query = select(User).where(User.phone == phone)
    return await db.scalar(query)

# Function to retrieve a user by their email
async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:
    query = select(User).where(User.email == email)
    return await db.scalar(query)

# Function to retrieve a user by their access token
async def get_user_by_token(db: AsyncSession, access_token: str) -> User | None:
    query = select(User).where(User.access_token == access_token)
    return await db.scalar(query)

# Function to create a new user in the database with the provided registration details, password hash, and tax ID
async def create_user(
    db: AsyncSession,
    payload: UserRegistrationRequest,
    password_hash: str,
    tax_id: str
) -> User:
    user = User(
        login=payload.phone,
        full_name=payload.full_name,
        phone=payload.phone,
        email=payload.email,
        birth_date=payload.birth_date,
        gender=payload.gender,
        tax_id=tax_id,
        password_hash=password_hash,
    )
    db.add(user)
    await db.flush()  # Ensure the operation is added to the session and assigned an ID
    return user
