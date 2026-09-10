import pytest
from decimal import Decimal


def as_decimal(value) -> Decimal:
    return Decimal(str(value))


async def register_and_login(client) -> dict[str, str]:
    registration_payload = {
        "full_name": "Іван Петренко",
        "phone": "+380501234567",
        "password": "StrongPassword123",
        "birth_date": "2000-01-01",
        "email": "ivan@example.com",
        "gender": "male",
    }
    
    registration_response = await client.post(
        "/api/v1/users",
        json=registration_payload
    )
    
    assert registration_response.status_code == 200
    
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "phone": registration_payload["phone"],
            "password": registration_payload["password"],
        }
    )
    
    assert login_response.status_code == 200
    
    access_token = login_response.json()["access_token"]
    
    return {
        "Authorization": f"Bearer {access_token}"
    }


async def create_card(
    client,
    headers: dict[str, str],
    payment_system: str,
    initial_balance: str,
) -> dict:
    response = await client.post(
        "/api/v1/cards",
        headers=headers,
        json={
            "payment_system": payment_system,
            "card_type": "debit",
            "currency": "uah",
            "initial_balance": initial_balance,
        },
    )
    
    assert response.status_code == 200
    
    return response.json()


@pytest.mark.asyncio
async def test_create_card(client) -> None:
    headers = await register_and_login(client)
    
    card = await create_card(
        client,
        headers,
        payment_system="visa",
        initial_balance="1000.0",
    )
    
    assert card["payment_system"] == "visa"
    assert card["card_type"] == "debit"
    assert card["currency"] == "uah"
    assert as_decimal(card["balance"]) == Decimal("1000.0")
    assert len(card["card_number"]) == 16


@pytest.mark.asyncio
async def test_expense_updates_balance_and_creates_operation(
    client,
) -> None:
    headers = await register_and_login(client)

    card = await create_card(
        client,
        headers,
        payment_system="visa",
        initial_balance="1000.00",
    )

    operation_response = await client.post(
        "/api/v1/operation",
        headers=headers,
        json={
            "card_id": card["id"],
            "type": "expense",
            "amount": "250.50",
            "currency": "uah",
            "category": "Food",
            "subcategory": "Products",
        },
    )

    assert operation_response.status_code == 200

    operation = operation_response.json()

    assert operation["card_id"] == card["id"]
    assert operation["type"] == "expense"
    assert as_decimal(operation["amount"]) == Decimal("250.50")
    assert operation["category"] == "Food"
    assert operation["subcategory"] == "Products"

    cards_response = await client.get(
        "/api/v1/cards",
        headers=headers,
    )

    assert cards_response.status_code == 200

    updated_card = cards_response.json()[0]

    assert as_decimal(updated_card["balance"]) == Decimal("749.50")

    operations_response = await client.get(
        "/api/v1/operations",
        headers=headers,
    )

    assert operations_response.status_code == 200

    operations = operations_response.json()

    assert len(operations) == 1
    assert operations[0]["id"] == operation["id"]
    assert operations[0]["type"] == "expense"


@pytest.mark.asyncio
async def test_transfer_updates_both_balances_and_creates_operations(
    client,
) -> None:
    headers = await register_and_login(client)

    source_card = await create_card(
        client,
        headers,
        payment_system="visa",
        initial_balance="1000.00",
    )

    destination_card = await create_card(
        client,
        headers,
        payment_system="mastercard",
        initial_balance="100.00",
    )

    transfer_response = await client.post(
        "/api/v1/operation/transfer",
        headers=headers,
        json={
            "from_card_id": source_card["id"],
            "to_card_id": destination_card["id"],
            "amount": "250.50",
            "currency": "uah",
        },
    )

    assert transfer_response.status_code == 200
    assert transfer_response.json() == {
        "message": "Transfer completed",
    }

    cards_response = await client.get(
        "/api/v1/cards",
        headers=headers,
    )

    cards_by_id = {
        card["id"]: card
        for card in cards_response.json()
    }

    assert as_decimal(
        cards_by_id[source_card["id"]]["balance"]
    ) == Decimal("749.50")

    assert as_decimal(
        cards_by_id[destination_card["id"]]["balance"]
    ) == Decimal("350.50")

    operations_response = await client.get(
        "/api/v1/operations",
        headers=headers,
    )

    operations = operations_response.json()

    assert len(operations) == 2
    assert {operation["type"] for operation in operations} == {
        "transfer",
    }
    assert {
        operation["category"]
        for operation in operations
    } == {"Transfer"}

    assert {
        operation["subcategory"]
        for operation in operations
    } == {"Deduction", "Credit"}