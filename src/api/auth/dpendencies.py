from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.core.jwt_utils import decode_access_token
from src.database.sessions import get_db
from src.database.schemas import User

# Reusable bearer scheme – this will show the "Authorize" button in Swagger UI
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    FastAPI dependency that:
    1. Extracts the Bearer token from the Authorization header.
    2. Decodes and validates the access token.
    3. Fetches and returns the matching User from the database.
    """
    token = credentials.credentials
    payload = decode_access_token(token)  # raises HTTP 417 on invalid/expired token

    user_id: int | None = payload.get("user", {}).get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that allows access only to admin users.
    Use this instead of get_current_user on admin-only endpoints.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required.",
        )
    return current_user
