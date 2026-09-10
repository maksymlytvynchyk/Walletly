import pytest
import re
from unittest.mock import AsyncMock
from app.enum import PaymentSystemEnum
from app.service.cards import generate_luhn_digit, get_payment_system_digit, generate_card_number, generate_demo_iban
from app.repository import cards as cards_repository


@pytest.mark.asyncio
async def test_generate_luhn_digit() -> None:
    # Test cases for Luhn digit generation
    test_cases = {
        "7992739871": "3",  # Example from Luhn algorithm
        "123456781234567": "0",  # Valid number with Luhn digit 0
        "123456781234568": "8",  # Valid number with Luhn digit 7
    }

    for number, expected_luhn in test_cases.items():
        assert await generate_luhn_digit(number) == int(expected_luhn)
        

def test_payment_system_digit() -> None:
    assert get_payment_system_digit(PaymentSystemEnum.VISA) == "4"
    assert get_payment_system_digit(PaymentSystemEnum.MASTERCARD) == "5"

def test_wrong_payment_system_digit() -> None:
    with pytest.raises(ValueError, match="Unsupported payment system"):
        get_payment_system_digit("wrong_payment_system")
    
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("payment_system", "prefix"),
    [
        (PaymentSystemEnum.VISA, "4"),
        (PaymentSystemEnum.MASTERCARD, "5"),
    ],
)
async def test_generate_card_number_has_valid_format(monkeypatch, payment_system, prefix) -> None:
    monkeypatch.setattr(
        cards_repository,
        "get_cards_by_bank_code",
        AsyncMock(return_value=[]),
    )
    
    card_number = await generate_card_number(
        db=None,
        payment_system=payment_system,
    )
    
    assert re.fullmatch(r"\d{16}", card_number)
    assert card_number.startswith(prefix)
