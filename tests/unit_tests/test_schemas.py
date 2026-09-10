import pytest
from datetime import date
from decimal import Decimal

from pydantic import ValidationError
from app.schemas import (
    CreateCardRequest,
    OperationRequest,
    TransferCreateSchema,
    UserRegistrationRequest,
)


def valid_registration_data() -> dict:
    return {
        "full_name": "Петренко Іван  Олексійович",
        "phone": "+380 50 123-45-67",
        "password": "test_password",
        "birth_date": date(2000, 1, 1),
        "email": "IVAN@test.com",
        "gender": "male",
    }


def test_registration_normilizes_phone_and_email() -> None:
    user = UserRegistrationRequest(**valid_registration_data())
    
    assert user.full_name == "Петренко Іван Олексійович"
    assert user.phone == "+380501234567"
    assert user.email == "ivan@test.com"
    

@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("phone", "abc"),
        ("email", "not-an-email"),
        ("password", "short"),
        ("birth_date", date.today()),
    ],
)
def test_registration_rejects_invalid_data(
    field: str,
    value: str | date,
) -> None:
    data = valid_registration_data()
    data[field] = value

    with pytest.raises(ValidationError):
        UserRegistrationRequest(**data)
        

def test_card_rejects_negative_initial_balance() -> None:
    with pytest.raises(ValidationError):
        CreateCardRequest(
            payment_system="visa",
            card_type="debit",
            currency="uah",
            initial_balance=Decimal("-0.01"),
        )


def test_operation_rejects_zero_amount() -> None:
    with pytest.raises(ValidationError):
        OperationRequest(
            card_id=1,
            type="income",
            amount=Decimal("0"),
            currency="uah",
        )


def test_transfer_rejects_same_card() -> None:
    with pytest.raises(ValidationError):
        TransferCreateSchema(
            from_card_id=1,
            to_card_id=1,
            amount=Decimal("100.00"),
            currency="uah",
        )