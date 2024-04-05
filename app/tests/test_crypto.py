from src.api.auth.crypto import (
    get_password_hash,
    check_password_hash,
    create_access_token,
    verify_access_token,
)


def test_generate_password_hash():
    password_hash = get_password_hash("password")
    assert len(password_hash) == 60


def test_verify_password_hash():
    password_hash = get_password_hash("password")
    assert check_password_hash("password", password_hash) is True
    assert check_password_hash("wrong", password_hash) is False


def test_generate_access_token():
    token = create_access_token({"test": "test"})
    assert isinstance(token, str) is True


def test_verify_access_token():
    token = create_access_token({"test": "test"})
    assert verify_access_token(token) == {"test": "test"}
    assert verify_access_token(token) != {"wrong": "wrong"}
