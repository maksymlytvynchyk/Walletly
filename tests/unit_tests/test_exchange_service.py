import pytest

from decimal import Decimal
from app.enum import CurrencyEnum
from app.service import exchange_service


def test_fallback_rate_is_decimal_and_exact() -> None:
    rate = exchange_service.FALLBACK_RATES[
        (CurrencyEnum.USD, CurrencyEnum.UAH)
    ]
    
    assert rate == Decimal("46.92")
    assert isinstance(rate, Decimal)


class FailingSession:
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        return None
    
    def get(self, url):
        raise RuntimeError("Network is unavailable")


@pytest.mark.asyncio
async def test_get_exchange_rate_uses_fallback_when_request_fails(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        exchange_service.aiohttp,
        "ClientSession",
        lambda timeout: FailingSession(),
    )
    
    rate = await exchange_service.get_exchange_rate(
        CurrencyEnum.USD,
        CurrencyEnum.UAH,
    )
    
    assert rate == Decimal("46.92")