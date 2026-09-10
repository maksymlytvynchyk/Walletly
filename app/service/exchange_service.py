from decimal import Decimal
from typing import Dict, Tuple
import aiohttp
from app.enum import CurrencyEnum

FALLBACK_RATES: Dict[Tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.UAH): Decimal("46.92"),
    (CurrencyEnum.EUR, CurrencyEnum.UAH): Decimal("49.92"),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal("0.92"),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal("1.08"),
    (CurrencyEnum.UAH, CurrencyEnum.USD): Decimal("0.0213"),
    (CurrencyEnum.UAH, CurrencyEnum.EUR): Decimal("0.0200"),
}

# Service function to get the exchange rate between two currencies, using an external API with a fallback to predefined rates
async def get_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
    
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/latest/currencies/{base}.json"
    
    timeout = aiohttp.ClientTimeout(total=5.0)  # Set a timeout of 5 seconds
    
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Raise an exception for HTTP errors
                data = await response.json()
                base_map = data.get(base, {})
                rate = base_map.get(target)
        
        if rate is not None and isinstance(rate, (int, float)):
            return Decimal(rate)
        raise KeyError("Rate not found")

    except Exception:
        # If the API call fails, return a fallback rate from the predefined dictionary
        return FALLBACK_RATES.get((base, target), Decimal("1"))
    
    
    
    