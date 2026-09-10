from enum import StrEnum, auto

# Enums for various constants used in the application
# Enums for currencies
class CurrencyEnum(StrEnum):
    UAH = auto()
    USD = auto()
    EUR = auto()

# Enums for payment systems
class PaymentSystemEnum(StrEnum):
    VISA = "visa"
    MASTERCARD = "mastercard"

# Enums for card types
class CardTypeEnum(StrEnum):
    DEBIT = "debit"
    CREDIT = "credit"
    OVERDRAFT = "overdraft"

# Enums for operation types
class OperationTypeEnum(StrEnum):
    EXPENSE = auto()
    INCOME = auto()
    TRANSFER = auto()

# Enums for gender
class GenderEnum(StrEnum):
    MALE = "male"
    FEMALE = "female"

# Enums for bank codes
class BankCodeEnum(StrEnum):
    DEMO_BANK = "2340068"