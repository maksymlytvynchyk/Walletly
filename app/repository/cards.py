from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from app.enum import CardTypeEnum, CurrencyEnum, PaymentSystemEnum
from app.models import Card

# Repository functions for managing card-related operations, including checking existence, adding income/expense, retrieving cards, and creating new cards
# Function to check if a card exists for a given user by card number
async def is_card_exist(db: AsyncSession, user_id: int, card_number: str) -> bool:
    query = select(Card).where(Card.card_number == card_number, Card.user_id == user_id)
    return await db.scalar(query) is not None

# Income operation: add the amount to the card balance
async def add_income(db: AsyncSession, user_id: int, card_number: str, amount: Decimal) -> Card:
    query = select(Card).where(Card.card_number == card_number, Card.user_id == user_id)
    card = await db.scalar(query)
    card.balance += amount
    return card

# Expense operation: subtract the amount from the card balance
async def add_expense(db: AsyncSession, user_id: int, card_number: str, amount: Decimal) -> Card:
    query = select(Card).where(Card.card_number == card_number, Card.user_id == user_id)
    card = await db.scalar(query)
    card.balance -= amount
    return card

# Function to retrieve a card by its number for a given user
async def get_card_by_number(
    db: AsyncSession,
    card_number: str,
) -> Card | None:
    query = select(Card).where(
        Card.card_number == card_number
    )

    return await db.scalar(query)

# Function to retrieve a card by its IBAN for a given user
async def get_card_by_iban(
    db: AsyncSession,
    iban: str,
) -> Card | None:
    query = select(Card).where(
        Card.iban == iban
    )

    return await db.scalar(query)

# Function to retrieve all cards associated with a specific user, ordered by card ID
async def get_all_cards(
    db: AsyncSession,
    user_id: int,
) -> list[Card]:
    query = (
        select(Card)
        .where(Card.user_id == user_id)
        .order_by(Card.id)
    )

    result = await db.execute(query)

    return list(result.scalars().all())

# Function to retrieve a card by its ID for a given user
async def get_card_by_id(
    db: AsyncSession, 
    user_id: int, 
    card_id: int
) -> Card:
    query = select(Card).where(Card.id == card_id, Card.user_id == user_id)
    return await db.scalar(query)

# Function to retrieve all cards associated with a specific bank code, ordered by card ID
async def get_cards_by_bank_code(
    db: AsyncSession,
    bank_code: str,
) -> list[Card]:

    query = (
        select(Card)
        .where(Card.bank_code == bank_code)
        .order_by(Card.id)
    )

    result = await db.execute(query)

    return list(result.scalars().all())

# Function to create a new card in the database with the provided details, ensuring it is added to the session without committing
async def create_card(
    db: AsyncSession,
    user_id: int,
    card_number: str,
    iban: str,
    bank_code: str,
    cvv: str,
    expires_at: date,
    payment_system: PaymentSystemEnum,
    card_type: CardTypeEnum,
    balance: Decimal,
    currency: CurrencyEnum,
) -> Card:

    card = Card(
        user_id=user_id,
        card_number=card_number,
        iban=iban,
        bank_code=bank_code,
        cvv=cvv,
        expires_at=expires_at,
        payment_system=payment_system,
        card_type=card_type,
        balance=balance,
        currency=currency,
    )

    db.add(card)

    await db.flush()

    return card

