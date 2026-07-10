from passlib.context import CryptContext
from src.api.config import JWT_ALGORITHM,JWT_SECRET_KEY
import jwt 
from datetime import timedelta,datetime
from fastapi import HTTPException,status 

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hashed_password(password:str):
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)



