from pydantic import BaseModel, EmailStr

class User_Sign_Up(BaseModel):
    email: EmailStr
    password: str
    username: str

class User_Login(BaseModel):
    email: EmailStr
    password: str
