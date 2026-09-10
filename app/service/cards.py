from datetime import date
from decimal import Decimal
import secrets
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.enum import CurrencyEnum, PaymentSystemEnum, BankCodeEnum
from app.models import User
from app.schemas import CreateCardRequest, TotalBalance, CardResponse
from app.repository import cards as cards_repository
from app.service import exchange_service


# Function to generate the Luhn digit for a card number based on its first 15 digits
async def generate_luhn_digit(number: str) -> str:
    
    total = 0

    for index, digit in enumerate(reversed(number)):
        value = int(digit)

        if index % 2 == 0:
            value *= 2

            if value > 9:
                value -= 9

        total += value

    return (10 - (total % 10)) % 10

# Function to get the payment system digit based on the payment system enum
def get_payment_system_digit(
    payment_system: PaymentSystemEnum,
) -> str:
    """
    Visa -> 4
    Mastercard -> 5
    """

    if payment_system == PaymentSystemEnum.VISA:
        return "4"

    if payment_system == PaymentSystemEnum.MASTERCARD:
        return "5"

    raise ValueError("Unsupported payment system")

# Function to get the next card sequence number for a given payment system
async def get_next_card_sequence(
    db: AsyncSession,
    payment_system: PaymentSystemEnum,
) -> str:
    """
    Get the next card sequence number for a given payment system.
    """

    cards = await cards_repository.get_cards_by_bank_code(db, BankCodeEnum.DEMO_BANK.value)
    
    if not cards:
        return 0
    
    max_sequence = -1
    
    for card in cards:
        sequence = int(card.card_number[8:15])
        
        if sequence > max_sequence:
            max_sequence = sequence
    
    return max_sequence + 1

# Function to generate a unique card number
async def generate_card_number(
    db: AsyncSession,
    payment_system: PaymentSystemEnum,
) -> str:
    
    payment_system_digit = get_payment_system_digit(payment_system)
    sequence_number = await get_next_card_sequence(db, payment_system)
    if sequence_number > 9999999:
        raise ValueError("Maximum number of cards reached for this payment system")
    
    sequence_part = f"{sequence_number:07d}"
    
    first_15_digits = f"{payment_system_digit}{BankCodeEnum.DEMO_BANK.value}{sequence_part}"
    
    luhn_digit = await generate_luhn_digit(first_15_digits)
    return first_15_digits + str(luhn_digit)

# Function to generate a random CVV code for a card
def generate_cvv() -> str:
    return f"{secrets.randbelow(1000):03d}"

# Function to generate an expiration date for a card, set to 5 years from the current date
def generate_expiration_date() -> date:
    today = date.today()

    try:
        return today.replace(year=today.year + 5)
    except ValueError:
        return today.replace(
            year=today.year + 5,
            day=28,
        )

# Function to calculate the IBAN checksum for a given IBAN without the checksum
def calculate_iban_checksum(
    iban_without_checksum: str,
) -> str:

    rearranged = (
        iban_without_checksum[4:]
        + iban_without_checksum[:4]
    )

    numeric = ""

    for character in rearranged:

        if character.isdigit():
            numeric += character

        else:
            numeric += str(
                ord(character.upper()) - ord("A") + 10
            )

    remainder = int(numeric) % 97

    checksum = 98 - remainder

    return f"{checksum:02d}"

# Function to generate a demo IBAN for a card based on its card number
def generate_demo_iban(
    card_number: str,
) -> str:

    # Country code for Ukraine
    country_code = "UA"

    # Initial checksum value (will be calculated later)
    checksum = "00"

    account_number = (
        BankCodeEnum.DEMO_BANK.value
        + card_number[-10:]
    )

    iban_without_checksum = (
        country_code
        + checksum
        + account_number
    )

    checksum = calculate_iban_checksum(
        iban_without_checksum
    )

    return (
        country_code
        + checksum
        + account_number
    )

# Service function to create a new card for a user, ensuring uniqueness of card number and IBAN
async def create_card(
    db: AsyncSession,
    user_id: int,
    payload: CreateCardRequest,
) -> CardResponse:
    
    for _ in range(3):

        card_number = await generate_card_number(
            db,
            payload.payment_system,
        )

        existing_card = (
            await cards_repository.get_card_by_number(
                db,
                card_number,
            )
        )

        if existing_card:
            continue

        cvv = generate_cvv()

        expires_at = generate_expiration_date()

        iban = generate_demo_iban(card_number)

        existing_iban = (
            await cards_repository.get_card_by_iban(
                db,
                iban,
            )
        )

        if existing_iban:
            continue

        try:

            card = await cards_repository.create_card(
                db=db,
                user_id=user_id,
                card_number=card_number,
                iban=iban,
                bank_code=BankCodeEnum.DEMO_BANK,
                cvv=cvv,
                expires_at=expires_at,
                payment_system=payload.payment_system,
                card_type=payload.card_type,
                balance=payload.initial_balance,
                currency=payload.currency,
            )

            await db.commit()

            await db.refresh(card)

            return CardResponse.model_validate(card)

        except Exception as e:
            await db.rollback()
            print("REAL ERROR:", repr(e))
            raise
    raise HTTPException(
        status_code=409,
        detail="Could not generate a unique card after multiple attempts. Please try again later.",
    )

# Service function to calculate the total balance across all cards of a user, converting to UAH if necessary
async def get_total_balance(db: AsyncSession, current_user: User) -> TotalBalance:

    cards = await cards_repository.get_all_cards(db, current_user.id)
    total_balance = Decimal()
    for card in cards:
        if card.currency == CurrencyEnum.UAH:
            total_balance += card.balance
        else:
            # Convert to UAH using exchange rate
            exchange_rate = await exchange_service.get_exchange_rate(card.currency, CurrencyEnum.UAH)
            total_balance += card.balance * exchange_rate

    return TotalBalance(total_balance=total_balance)

# Service function to retrieve all cards for a user, returning them as a list of CardResponse objects
async def get_all_cards(db: AsyncSession, current_user: User) -> list[CardResponse]:
    cards = await cards_repository.get_all_cards(db, current_user.id)
    return [CardResponse.model_validate(card) for card in cards]
