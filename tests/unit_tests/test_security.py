from app.security import hash_password, verify_password


def test_hash_and_verify_password():
    password = "my_secure_password"
    hashed_password = hash_password(password)

    # Ensure the hashed password is not the same as the original password
    assert hashed_password != password

    # Verify that the original password matches the hashed password
    assert verify_password(password, hashed_password) is True

    
def test_verify_password_rejects_wrong_password() -> None:
    password = hash_password("correct_password")
    
    # Ensure that verifying a wrong password against the hashed password returns False
    assert verify_password("wrong_password", password) is False
    
    
def test_same_passwords_produce_different_hashes() -> None:
    password = "same_password"
    
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    # Ensure that two hashes of the same password are different due to random salt
    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


def test_verify_password_with_invalid_hash_format() -> None:
    invalid_hash = "invalid_format_hash"
    
    # Ensure that verifying a password against an invalid hash format returns False
    assert verify_password("any_password", invalid_hash) is False