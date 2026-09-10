import pytest
from app.service.cards import generate_demo_iban


def is_valid_iban(iban: str) -> bool:
    rearranged = iban[4:] + iban[:4]
    
    numeric_iban = "".join(
        character
        if character.isdigit()
        else str(ord(character.upper()) - ord("A") + 10)
        for character in rearranged
    )
    
    return int(numeric_iban) % 97 == 1

@pytest.mark.parametrize(
    "card_number",
    [
        "4234006800000000",
        "5234006800000000",
        "4234006812345678",
    ],
)
def test_generate_demo_iban(card_number: str) -> None:
    iban = generate_demo_iban(card_number)
    
    assert iban.startswith("UA")
    assert iban.isalnum()
    assert iban[4:] == "2340068" + card_number[-10:]
    assert is_valid_iban(iban)
    

def test_generate_demo_iban_deterministic() -> None:
    card_number = "4234006800000000"
    
    first_iban = generate_demo_iban(card_number)
    second_iban = generate_demo_iban(card_number)
    
    assert first_iban == second_iban