from pydantic import BaseModel,EmailStr,Field
from datetime import datetime


class UserProfile(BaseModel):
    user_id: int  # or UUID
    username: str
    email: EmailStr
    bio: str | None
    phone_number: str | None = None  # no pattern here — output schema shouldn't reject DB data
    profile_picture: str | None
    created_at: datetime
    updated_at: datetime



class UpdateUser(BaseModel):
    username: str | None = None
    bio: str | None = None
    phone_number: str | None = Field(default=None, pattern=r"^\d{10}$")
    email: EmailStr | None = None

class UpdateProfilePictureResponse(BaseModel):
    message: str


class GrantAdminRequest(BaseModel):
    user_id: int

