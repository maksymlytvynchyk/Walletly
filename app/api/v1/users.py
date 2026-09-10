from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import AuthResponse, UserLoginRequest, UserRegistrationRequest, UserResponse
from app.service import users as users_service
from app.dependency import get_current_user, get_db

router = APIRouter()

# API endpoint to create a new user, accepting a registration request and returning the created user's details
@router.post("/users", response_model=UserResponse)
async def create_user(payload: UserRegistrationRequest, db: AsyncSession = Depends(get_db)):
    return await users_service.create_user(db, payload)

# API endpoint for user login, accepting login credentials and returning an authentication response with an access token
@router.post("/auth/login", response_model=AuthResponse)
async def login(payload: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    return await users_service.login_user(db, payload)

# API endpoint to retrieve the current authenticated user's details, requiring a valid access token for authorization
@router.get("/users/me", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
