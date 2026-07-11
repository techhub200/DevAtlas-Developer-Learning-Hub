from pydantic import BaseModel, EmailStr

class User_Sign_Up(BaseModel):
    email: EmailStr
    password: str
    username: str
    phone_number: str | None = None
    bio: str | None = None


class User_Login(BaseModel):
    email: EmailStr
    password: str
