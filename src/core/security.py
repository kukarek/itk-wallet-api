from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.core.config import get_settings

settings = get_settings()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt.SECRET_KEY, algorithm=settings.jwt.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.jwt.SECRET_KEY, algorithms=[settings.jwt.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
