from datetime import datetime
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.enum import CurrencyEnum, OperationTypeEnum
from app.models import Card, Operation

# Repository functions for managing financial operations, including creating operations and retrieving operations by user or card IDs
# Function to create a new operation in the database with the provided details, ensuring it is added to the session without committing
async def create_operation(
    db: AsyncSession,
    card_id: int,
    operation_type: OperationTypeEnum,
    amount: Decimal,
    currency: CurrencyEnum,
    category: str | None = None,
    subcategory: str | None = None,
) -> Operation:
    operation = Operation(
        card_id=card_id,
        type=operation_type,
        amount=amount,
        currency=currency,
        category=category,
        subcategory=subcategory,
    )

    db.add(operation)

    await db.flush()

    return operation

# Function to retrieve all operations associated with a specific user, ordered by creation date in descending order
async def get_operations_by_user(
    db: AsyncSession,
    user_id: int,
) -> list[Operation]:
    query = (
        select(Operation)
        .join(Card, Operation.card_id == Card.id)
        .where(Card.user_id == user_id)
        .order_by(Operation.created_at.desc())
    )

    result = await db.execute(query)

    return list(result.scalars().all())

# Function to retrieve all operations associated with a list of card IDs, optionally filtered by a date range, and ordered by creation date in descending order
async def get_operations_by_cards(
    db: AsyncSession,
    card_ids: list[int],
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[Operation]:

    if not card_ids:
        return []

    query = (
        select(Operation)
        .where(Operation.card_id.in_(card_ids))
        .order_by(Operation.created_at.desc())
    )

    if date_from is not None:
        query = query.where(Operation.created_at >= date_from)

    if date_to is not None:
        query = query.where(Operation.created_at <= date_to)

    result = await db.execute(query)

    return list(result.scalars().all())