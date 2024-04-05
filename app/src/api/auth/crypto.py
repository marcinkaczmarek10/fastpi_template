from datetime import timedelta, datetime
from passlib.context import CryptContext
from jose import JWTError, jwt
from src.core.config import settings

ALGORITHM = "HS256"
crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return crypto_context.hash(password)


def check_password_hash(password: str, password_hash: str) -> bool:
    return crypto_context.verify(password, password_hash)


def create_access_token(data: dict, timedelta_to_expire: timedelta | None = None) -> str:
    data_to_encode = data.copy()
    if timedelta_to_expire:
        expiration_key = "exp"
        expiration_time = datetime.utcnow() + timedelta_to_expire
        data_to_encode.update({expiration_key: expiration_time})
    encoded_jwt = jwt.encode(
        claims=data_to_encode, key=settings.SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str) -> dict | None:
    return jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=ALGORITHM)
