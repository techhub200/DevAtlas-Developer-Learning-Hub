from fastapi import APIRouter, Depends
from src.api.auth.schemas import User_Sign_Up,User_Login
from datetime import timedelta
from src.core.jwt import create_access_token, create_refresh_token
auth_router = APIRouter()

@auth_router.post("/Register")
async def User_Register(User:User_Sign_Up):
  email= User.email
  password =User.password
  username = User.username
  pass 

@auth_router.post("/login")
async def user_login(user: User_Login):
    email = user.email
    password = user.password

    user_payload = {
        "email": email
    }
    access_token = create_access_token(
        user_payload,
        timedelta(minutes=15)
    )

    refresh_token = create_refresh_token(
        user_payload,
        timedelta(days=7)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }