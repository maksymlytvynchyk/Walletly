from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependency import get_current_user, get_db
from app.models import User
from app.service import cards as cards_service
from app.schemas import CreateCardRequest, CardResponse

router = APIRouter()

# API endpoint to retrieve the total balance of the current authenticated user's cards, requiring a valid access token for authorization
@router.get("/balance")
async def get_total_balance(db: AsyncSession = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return await cards_service.get_total_balance(db, current_user)

# API endpoint to create a new card for the current authenticated user, accepting card details and returning the created card's information
@router.post("/cards", response_model=CardResponse)
async def create_card(card: CreateCardRequest, db: AsyncSession = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return await cards_service.create_card(db, current_user.id, card)

# API endpoint to retrieve all cards associated with the current authenticated user, requiring a valid access token for authorization
@router.get("/cards", response_model=list[CardResponse])
async def get_all_cards(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await cards_service.get_all_cards(db, current_user)