
from datetime import date, datetime, timezone
from decimal import Decimal
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from app.database import Base
from app.enum import BankCodeEnum, CardTypeEnum, CurrencyEnum, GenderEnum, OperationTypeEnum, PaymentSystemEnum

# User model in database
class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    # Kept for compatibility with the existing database; it mirrors phone.
    login: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str] = mapped_column(default="")
    phone: Mapped[str] = mapped_column(unique=True, index=True, default="")
    email: Mapped[str] = mapped_column(unique=True, index=True, default="")
    birth_date: Mapped[date | None] = mapped_column(nullable=True)
    gender: Mapped[GenderEnum] = mapped_column()
    tax_id: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column(default="")
    access_token: Mapped[str | None] = mapped_column(unique=True, index=True, nullable=True)

# Card model in database
class Card(Base):
    __tablename__ = "card"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True)
    card_number: Mapped[str] = mapped_column(unique=True, index=True)
    iban: Mapped[str] = mapped_column(unique=True, index=True)
    bank_code: Mapped[BankCodeEnum] = mapped_column(default=BankCodeEnum.DEMO_BANK, nullable=False)
    cvv: Mapped[str] = mapped_column()
    expires_at: Mapped[date] = mapped_column()
    payment_system: Mapped[PaymentSystemEnum] = mapped_column()
    card_type: Mapped[CardTypeEnum] = mapped_column()
    balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"), nullable=False)
    currency: Mapped[CurrencyEnum] = mapped_column(default=CurrencyEnum.UAH, nullable=False)
    
# Operation model in database
class Operation(Base):
    __tablename__ = "operation"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("card.id"), nullable=False, index=True)
    type: Mapped[OperationTypeEnum] = mapped_column()
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    currency: Mapped[CurrencyEnum] = mapped_column()
    category: Mapped[str | None] = mapped_column(default=None)
    subcategory: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
