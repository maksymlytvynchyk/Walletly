# Walletly

A full-stack pet project for personal finance management. Users can create demo cards, record income and expenses, transfer money between cards, and review their transaction history.

This is an educational project. It does not process real payments and must not be used to store real banking data.

## Features

- User registration and authentication.

- Validation of full name, phone number, email, date of birth, and password.

- Creation of demo Visa and Mastercard cards.

- Card number generation using the Luhn algorithm.

- Demo IBAN generation.

- Support for UAH, USD, and EUR.

- Income and expense tracking.

- Transfers between cards in the same currency.

- Transaction history.

- Total balance calculation in UAH.

- Exchange-rate retrieval with fallback values.

- Ukrainian-language Vue interface.

Tech Stack

#### Backend

- Python

- FastAPI

- Async SQLAlchemy

- PostgreSQL

- asyncpg

- Pydantic

- Alembic

- pytest

#### Frontend

- Vue 3

- Vite

- Tailwind CSS

- JavaScript

## Project Structure

```text
FastAPI/
├── app/
│   ├── api/               # API routes
│   ├── repository/        # Database access layer
│   ├── service/           # Business logic
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   └── security.py        # Password hashing
│
├── alembic/               # Alembic migrations
├── frontend/              # Vue application
├── tests/
│   ├── unit_tests/        # Unit tests
│   └── integration_tests/ # API and PostgreSQL integration tests
│
├── main.py
├── requirements.txt
└── alembic.ini
```

## Installation and Setup

1. Clone the repository

```text
git clone https://github.com/maksymlytvynchyk/Walletly.git
cd FastAPI
```

2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

4. Create an environment file

Create .env in the project root:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=finance_db
DB_USER=postgres
DB_PASSWORD=your_password
```

5. Create the PostgreSQL database

```sql
CREATE DATABASE finance_db;
```

6. Apply migrations

```powershell
alembic upgrade head
```

7. Run the backend

```powershell
uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Running the Frontend in Development Mode

```powershell
cd frontend
npm install
npm run dev
```

Vite runs the frontend and proxies /api requests to FastAPI.

Frontend Production Build

```powershell
cd frontend
npm run build
```

After the build, FastAPI serves the frontend from frontend/dist.

## API Endpoints

```text
Method

Endpoint

Description

POST

/api/v1/users

Register a user

POST

/api/v1/auth/login

Authenticate and receive an access token

GET

/api/v1/users/me

Get the current user profile

POST

/api/v1/cards

Create a card

GET

/api/v1/cards

Get all cards for the current user

GET

/api/v1/balance

Get the total balance in UAH

POST

/api/v1/operation

Create an income or expense operation

POST

/api/v1/operation/transfer

Transfer money between cards

GET

/api/v1/operations

Get transaction history
```

Testing

Unit tests

```powershell
pytest tests/unit_tests -v
```

Integration tests

Create a dedicated test database:

```sql
CREATE DATABASE finance_test;
```

Create .env.test:

```env
TEST_DATABASE_URL=postgresql+asyncpg://postgres:your_password@127.0.0.1:5432/finance_test
```

Run the tests:

```powershell
pytest tests/integration_tests -v
```

Integration tests use a separate PostgreSQL database and Alembic migrations.

## Limitations and Future Improvements

- Cross-currency transfers with exchange-rate conversion.

- Pagination and filtering for transaction history.

- Logout, token expiration, and session revocation.

- Docker Compose for FastAPI, PostgreSQL, and the frontend.

- GitHub Actions CI.

- End-to-end tests with Playwright.

- Masking card data in API responses.

- Demo card data only.

Author

GitHub: https://github.com/maksymlytvynchyk/Walletly.git