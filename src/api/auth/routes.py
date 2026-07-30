from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from src.api.auth.dependencies import get_token_payload
from src.core.jwt_utils import create_access_token, create_refresh_token
from src.database.redis import add_access_token_to_blacklist
from src.database.sessions import get_db
from src.database.schemas import User
from src.core.utils import generate_hashed_password, verify_password
from src.api.auth.schemas import User_Login,User_Sign_Up

auth_router = APIRouter()


@auth_router.post("/Register", status_code=status.HTTP_201_CREATED)
async def user_register(user_data: User_Sign_Up, db: Session = Depends(get_db)):
    # Check if email or username already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )

    hashed_password = generate_hashed_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        bio=user_data.bio,
        phone_number=user_data.phone_number,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


@auth_router.post("/login")
async def user_login(user: User_Login, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password against the stored hash
    if not verify_password(user.password, existing.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    user_payload = {"user_id": existing.id, "email": existing.email}

    access_token = create_access_token(user_payload, timedelta(minutes=15))
    refresh_token = create_refresh_token(user_payload, timedelta(days=7))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }


@auth_router.post("/Logout")
async def User_Logout(token_data: dict = Depends(get_token_payload)):
    payload = token_data["payload"]

    jti = payload["jti"]
    exp_dt = datetime.fromtimestamp(payload["exp"])

    add_access_token_to_blacklist(
        jti=jti,
        exp=exp_dt,
    )

    return {"message": "Logged out (access token revoked)"}
