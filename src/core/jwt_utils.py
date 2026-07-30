

import uuid

from src.core.config import JWT_ALGORITHM, JWT_SECRET_KEY
import jwt
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status


def create_json_web_token(token_type: str, user_details: dict, expiry: timedelta) -> str:
    payload = {
        "type": token_type,
        "user": user_details,
        "jti": str(uuid.uuid4()),
        "exp": datetime.now(timezone.utc) + expiry,
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    # PyJWT may return bytes depending on version/config
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def create_access_token(user: dict, expiry: timedelta) -> str:
    return create_json_web_token("access", user, expiry)


def create_refresh_token(user: dict, expiry: timedelta) -> str:
    return create_json_web_token("refresh", user, expiry)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Token not decoded",
        ) from e


def decode_access_token(token: str) -> dict:
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type: expected access token",
        )
    return payload


def decode_refresh_token(token: str) -> dict:
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type: expected refresh token",
        )
    return payload
