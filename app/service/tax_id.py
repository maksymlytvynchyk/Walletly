from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.enum import GenderEnum
from app.models import User

# Service function to generate a unique tax ID based on birth date and gender
async def generate_tax_id(
    db: AsyncSession,
    birth_date: date,
    gender: GenderEnum,
) -> str:
    base_date = date(1899, 12, 31)
    days_since_base = (birth_date - base_date).days
    
    if days_since_base < 0 or days_since_base > 99999:
        raise ValueError("Birth date is out of valid range for tax ID generation")
    
    first_five_digits = f"{days_since_base:05d}"
    
    result = await db.execute(
        select(User.tax_id)
        .where(
            User.birth_date == birth_date,
            User.gender == gender,
            User.tax_id.is_not(None),
        )
    )
    
    tax_ids = result.scalars().all()
    
    if not tax_ids:
        sequence = 1 if gender == GenderEnum.MALE else 2
    else:
        last_tax_id = max(tax_ids)
        last_sequence = int(last_tax_id[5:9])
        sequence = last_sequence + 2
    
    sequence_part = f"{sequence:04d}"
    
    base_tax_id = f"{first_five_digits}{sequence_part}"
    
    control_digit = calculate_control_digit(base_tax_id)
    
    return f"{base_tax_id}{control_digit}"

# Function to calculate the control digit for a tax ID based on its first 9 digits
def calculate_control_digit(tax_id_without_control: str) -> str:
    if len(tax_id_without_control) != 9 or not tax_id_without_control.isdigit():
        raise ValueError("Tax ID without control digit must be 9 digits long")
    
    coefficients = [-1, 5, 7, 9, 4, 6, 10, 5, 7]
    
    total = sum(
        int(digit) * coefficient
        for digit, coefficient in zip(tax_id_without_control, coefficients)
    )
    
    return (total % 11) % 10