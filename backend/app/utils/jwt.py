from jose import jwt
from datetime import datetime, timedelta

from app.config.settings import settings

JWT_SECRET = settings.SECRET_KEY or settings.JWT_SECRET
JWT_ALGORITHM = settings.ALGORITHM or "HS256"


def create_access_token(data):
    payload = data.copy()
    payload["type"] = "access"
    payload["exp"] = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_refresh_token(data, jti: str):
    payload = data.copy()
    payload["type"] = "refresh"
    payload["jti"] = jti
    payload["exp"] = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
