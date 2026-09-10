import base64
import hashlib
import hmac
import os

# Security functions for password hashing and verification
def hash_password(password: str) -> str:
    salt = os.urandom(16)
    password_hash = hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1
    )
    return f"scrypt${base64.b64encode(salt).decode()}${base64.b64encode(password_hash).decode()}"

# Verify a password against a stored hash
def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, encoded_salt, encoded_hash = stored_hash.split("$", 2)
        if algorithm != "scrypt":
            return False
        calculated_hash = hashlib.scrypt(
            password.encode("utf-8"),
            salt=base64.b64decode(encoded_salt),
            n=2**14,
            r=8,
            p=1,
        )
        return hmac.compare_digest(
            calculated_hash,
            base64.b64decode(encoded_hash),
        )
    except (ValueError, TypeError):
        return False
