from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.core.jwt_utils import decode_access_token
from src.database.sessions import get_db
from src.database.schemas import User
from fastapi import Request

# Reusable bearer scheme – this will show the "Authorize" button in Swagger UI
bearer_scheme = HTTPBearer()

class Access_Token_Bearer(HTTPBearer):
    def __init__(self):
        # Ensure FastAPI doesn't auto-return 403/401 before we can log details.
        super().__init__(auto_error=False)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        if credentials is None or not credentials.credentials:
            # Header missing or not in Bearer format.
            print("[Auth] Missing/invalid Authorization header (expected: Bearer <token>)", flush=True)
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        token_str = credentials.credentials
        try:
            payload = decode_access_token(token_str)
            return {"token": token_str, "payload": payload}
        except Exception as e:
            # decode_access_token is responsible for logging exact jwt errors.
            print(f"[Auth] decode_access_token failed: {type(e).__name__}: {e}", flush=True)
            raise HTTPException(status_code=401, detail="Invalid or expired token")




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


def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """
    FastAPI dependency that extracts and decodes the Bearer token,
    returning the full payload dict including 'jti', 'exp', etc.
    Use this for endpoints like logout that need token metadata.
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    return {"token": token, "payload": payload}


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

