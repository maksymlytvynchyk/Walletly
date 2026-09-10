from datetime import date, datetime
import re

from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

from app.enum import CardTypeEnum, CurrencyEnum, GenderEnum, OperationTypeEnum, PaymentSystemEnum


# Model for description money operations

# User registration request model
class UserRegistrationRequest(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=127)
    phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)
    birth_date: date
    email: str = Field(..., max_length=255)
    gender: GenderEnum = Field(..., pattern="^(male|female)$")

    @field_validator("full_name")
    @classmethod
    def full_name_is_valid(cls, value: str) -> str:
        value = " ".join(value.split())
        is_value_correct = value.split(" ")
        if not value:
            raise ValueError("Full name cannot be empty")
        if len(is_value_correct) != 3:
            raise ValueError("Incorrect full name format; example: Ivan Ivanovych Petrenko")
        return value

    @field_validator("phone")
    @classmethod
    def phone_is_valid(cls, value: str) -> str:
        normalized = re.sub(r"[\s()\-]", "", value)
        if not re.fullmatch(r"\+?\d{10,15}", normalized):
            raise ValueError("Enter a valid phone number")
        return normalized

    @field_validator("email")
    @classmethod
    def email_is_valid(cls, value: str) -> str:
        value = value.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Enter a valid email")
        return value

    @field_validator("birth_date")
    @classmethod
    def birth_date_is_valid(cls, value: date) -> date:
        today = date.today()

        if value >= today:
            raise ValueError("Birth date must be in the past")

        age = today.year - value.year

        if (today.month, today.day) < (value.month, value.day):
            age -= 1

        if age < 14:
            raise ValueError("User must be at least 14 years old")

        return value
    
    @field_validator("gender")
    @classmethod
    def gender_is_valid(cls, value: str) -> str:
        if value not in ["male", "female"]:
            raise ValueError("Gender must be either 'male' or 'female'")
        return value

# User login request model
class UserLoginRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=1, max_length=128)

    @field_validator("phone")
    @classmethod
    def phone_is_valid(cls, value: str) -> str:
        normalized = re.sub(r"[\s()\-]", "", value)
        if not re.fullmatch(r"\+?\d{10,15}", normalized):
            raise ValueError("Enter a valid phone number")
        return normalized

# User response model
class UserResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    full_name: str
    phone: str
    email: str
    birth_date: date | None
    gender: GenderEnum
    tax_id: str

# Authentication response model
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Card creation request model
class CreateCardRequest(BaseModel):
    payment_system: PaymentSystemEnum
    card_type: CardTypeEnum
    currency: CurrencyEnum
    initial_balance: Decimal = Field(default=Decimal("0"))
    
    @field_validator("initial_balance")
    @classmethod
    def validate_initial_balance(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("Початковий баланс не може бути від'ємним")

        return value

# Card response model
class CardResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    card_number: str
    iban: str
    bank_code: str
    cvv: str
    expires_at: date
    payment_system: PaymentSystemEnum
    card_type: CardTypeEnum
    balance: Decimal
    currency: CurrencyEnum

# Operation request and response models
class OperationRequest(BaseModel):
    card_id: int
    type: OperationTypeEnum
    amount: Decimal
    currency: CurrencyEnum
    category: str | None = None
    subcategory: str | None = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("Amount must be positive")
        return value

# Operation response model
class OperationResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    card_id: int
    type: str
    amount: Decimal
    currency: CurrencyEnum
    category: str | None = None
    subcategory: str | None = None
    created_at: datetime

# Transfer request model
class TransferCreateSchema(BaseModel):
    from_card_id: int
    to_card_id: int
    amount: Decimal
    currency: CurrencyEnum

    @field_validator('amount')
    @classmethod
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        # Check is value positive
        if v <= 0:
            raise ValueError("Amount must be positive")
        # Return value if it's positive
        return v

    @field_validator('from_card_id', 'to_card_id')
    @classmethod
    def card_ids_must_be_different(cls, v: int, info) -> int:
        # Check if card ids are different
        if "from_card_id" in info.data and v == info.data["from_card_id"]:
            raise ValueError("Same cards ids")
        return v

# Total balance response model
class TotalBalance(BaseModel):
    total_balance: Decimal
