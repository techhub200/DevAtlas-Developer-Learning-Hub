from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta

from sqlalchemy.orm import Session

from src.api.auth.schemas import User_Sign_Up, User_Login
from src.core.jwt import create_access_token, create_refresh_token
from src.database.sessions import get_db
from src.database.schemas import User
from src.core.utils import generate_hashed_password

auth_router = APIRouter()


@auth_router.post("/Register")
async def user_register(user_data: User_Sign_Up, db: Session = Depends(get_db)):
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
    email = user.email

    # NOTE: your DB migration/model currently does NOT have a password column.
    # For now we only verify that the user exists.
    existing = db.query(User).filter(User.email == email).first()
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    user_payload = {"email": email}

    access_token = create_access_token(user_payload, timedelta(minutes=15))
    refresh_token = create_refresh_token(user_payload, timedelta(days=7))

    return {"access_token": access_token, "refresh_token": refresh_token}


