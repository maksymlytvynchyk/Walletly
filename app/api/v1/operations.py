from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_current_user, get_db
from app.models import User
from app.schemas import (
    OperationRequest,
    OperationResponse,
    TransferCreateSchema,
)
from app.service import operations as operations_service

router = APIRouter()

# API endpoint to create a new financial operation, accepting an operation request and returning the created operation's details
@router.post("/operation", response_model=OperationResponse)
async def create_operation(
    payload: OperationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await operations_service.create_operation(
        db=db,
        user_id=current_user.id,
        payload=payload,
    )

# API endpoint to transfer funds between cards, accepting a transfer request and returning a confirmation message upon successful completion
@router.post("/operation/transfer", response_model=None,)
async def transfer(
    payload: TransferCreateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await operations_service.transfer(
        db=db,
        user_id=current_user.id,
        payload=payload,
    )

    return {
        "message": "Transfer completed",
    }

# API endpoint to retrieve all financial operations associated with the current authenticated user, returning a list of operation responses
@router.get("/operations", response_model=list[OperationResponse],)
async def get_operations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await operations_service.get_user_operations(
        db=db,
        user_id=current_user.id,
    )