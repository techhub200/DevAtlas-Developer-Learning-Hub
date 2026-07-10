from fastapi import APIRouter, Depends
from auth.schemas import User_Sign_Up,User_Login
auth_router = APIRouter()

@auth_router.post("/Register")
async def User_Register(User:User_Sign_Up):
  email= User.email
  password =User.password
  username = User.username
  pass 

@auth_router.login("/Login")
async def User_Login(User:User_Login):
  email= User.email
  password =User.password
  pass 
