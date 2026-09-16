from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.enum import OperationTypeEnum
from app.repository import cards as cards_repository
from app.repository import operations as operations_repository
from app.schemas import (
    OperationRequest,
    OperationResponse,
    TransferCreateSchema,
)
from app.service.exchange_service import get_exchange_rate

# Service functions for managing financial operations, including creating operations and transferring funds between cards


async def create_operation(
    db: AsyncSession,
    user_id: int,
    payload: OperationRequest,
) -> OperationResponse:

    # Get the card by ID
    card = await cards_repository.get_card_by_id(
        db,
        user_id,
        payload.card_id,
    )

    if not card:
        raise HTTPException(
            status_code=404,
            detail={
                "field": "card_id",
                "code": "card_not_found",
            },
        )

    # Check if the card belongs to the user
    if card.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail={
                "field": "card_id",
                "code": "card_not_belong_to_user",
            },
        )

    # The currency of the operation must match
    # the currency of the card
    if card.currency != payload.currency:
        raise HTTPException(
            status_code=400,
            detail={
                "field": "currency",
                "code": "invalid_currency",
            },
        )

    # Income operation: add the amount to the card balance
    if payload.type == OperationTypeEnum.INCOME:
        card.balance += payload.amount

    # Expense operation: subtract the amount from the card balance
    elif payload.type == OperationTypeEnum.EXPENSE:

        if card.balance < payload.amount:
            raise HTTPException(
                status_code=400,
                detail={
                    "field": "amount",
                    "code": "not_enough_funds",
                },
            )

        card.balance -= payload.amount

    # Transfer operation: not allowed here, use the transfer endpoint
    # elif payload.type == OperationTypeEnum.TRANSFER:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="For transfers, use the dedicated endpoint",
    #     )

    # Create the operation record in the database
    operation = await operations_repository.create_operation(
        db=db,
        card_id=card.id,
        operation_type=payload.type,
        amount=payload.amount,
        currency=payload.currency,
        category=payload.category,
        subcategory=payload.subcategory,
    )

    # Commit the transaction to save changes to the database
    await db.commit()

    # Refresh the operation instance to get the latest data from the database
    await db.refresh(operation)

    return OperationResponse.model_validate(operation)

# Service function to transfer funds between two cards of the same user


async def transfer(
    db: AsyncSession,
    user_id: int,
    payload: TransferCreateSchema,
) -> None:
    # Check if the source and destination cards are the same
    if payload.from_card_id == payload.to_card_id:
        raise HTTPException(
            status_code=400,
            detail={
                "field": "card_id",
                "code": "same_cards_error",
            },
        )

    # Get the source card (from_card) by ID
    from_card = await cards_repository.get_card_by_id(
        db,
        user_id,
        payload.from_card_id,
    )

    if not from_card:
        raise HTTPException(
            status_code=404,
            detail={
                "field": "card_id",
                "code": "from_card_not_found",
            },
        )

    # Get the destination card (to_card) by ID
    to_card = await cards_repository.get_card_by_id(
        db,
        user_id,
        payload.to_card_id,
    )

    if not to_card:
        raise HTTPException(
            status_code=404,
            detail={
                "field": "card_id",
                "code": "to_card_not_found",
            },
        )

    # Check if both cards belong to the user
    if from_card.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail={
                "field": "card_id",
                "code": "from_card_not_belong_to_user",
            },
        )

    # Check if the source card has enough funds for the transfer
    if from_card.balance < payload.amount:
        raise HTTPException(
            status_code=400,
            detail={
                "field": "amount",
                "code": "not_enough_funds",
            },
        )

    target_amount = payload.amount
    if from_card.currency != to_card.currency:
        exchange_rate = await get_exchange_rate(from_card.currency, to_card.currency)
        target_amount = round(payload.amount * exchange_rate, 2)
    # Check if the transfer amount is positive
    from_card.balance -= payload.amount
    to_card.balance += target_amount

    # Create the operation records for both cards in the database
    await operations_repository.create_operation(
        db=db,
        card_id=from_card.id,
        operation_type=OperationTypeEnum.TRANSFER,
        amount=payload.amount,
        currency=payload.currency,
        category="Transfer",
        subcategory="Withdrawal",
    )

    # Create the operation record for the destination card
    await operations_repository.create_operation(
        db=db,
        card_id=to_card.id,
        operation_type=OperationTypeEnum.TRANSFER,
        amount=payload.amount,
        currency=payload.currency,
        category="Transfer",
        subcategory="Receipt",
    )

    # Finally, commit the transaction to save changes to the database
    await db.commit()

# Service function to retrieve all operations for a specific user


async def get_user_operations(
    db: AsyncSession,
    user_id: int,
) -> list[OperationResponse]:

    operations = await operations_repository.get_operations_by_user(
        db,
        user_id,
    )

    return [
        OperationResponse.model_validate(operation)
        for operation in operations
    ]
