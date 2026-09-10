from collections.abc import AsyncGenerator
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.models import User
from app.repository import users as users_repository

security = HTTPBearer()

# Function to obtain a database session via dependency injection
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
        
# Function to get the current user based on the provided credentials
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: AsyncSession = Depends(get_db)) -> User:
    user = await users_repository.get_user_by_token(db, credentials.credentials)
    
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return user
