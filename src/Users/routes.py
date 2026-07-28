from fastapi import APIRouter, Depends, UploadFile, File, status

from sqlalchemy.orm import Session
import shutil
import os
import uuid

from src.database.sessions import get_db
from src.database.schemas import User
from api.auth.dependencies import get_current_user
from src.Users.schemas import GrantAdminRequest
from src.Users.schemas import UpdateUser, UpdateProfilePictureResponse, UserProfile
from api.auth.dependencies import require_admin
from src.Error_Handling.errors import (
    UserAlreadyTaken,
    UserNameTaken,
    UserEmailTaken,
    Forbidden,
    NotFound,
    UnsupportedMediaType,
    RequestEntityTooLarge,
)



User_rotues = APIRouter()

# Directory to store uploaded profile pictures
UPLOAD_DIR = "uploads/profile_pictures"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@User_rotues.get("/Profile", response_model=UserProfile)
async def Get_User_Profile(current_user: User = Depends(get_current_user)):
    """Get the authenticated user's own profile."""
    return UserProfile(
        user_id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        bio=current_user.bio,
        phone_number=current_user.phone_number,
        profile_picture=current_user.profile_picture,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@User_rotues.put("/Update_Profile", response_model=UserProfile)
async def Update_Profile(
    update_data: UpdateUser,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the authenticated user's profile data.
    Only fields that are provided (non-None) are updated.
    """
    # Check for username conflict if a new username is supplied
    if update_data.username and update_data.username != current_user.username:
        existing = db.query(User).filter(User.username == update_data.username).first()
        if existing:
            raise UserNameTaken()

    # Check for email conflict if a new email is supplied
    if update_data.email and update_data.email != current_user.email:
        existing = db.query(User).filter(User.email == update_data.email).first()
        if existing:
            raise UserEmailTaken()


    # Apply only the supplied fields
    if update_data.username is not None:
        current_user.username = update_data.username
    if update_data.bio is not None:
        current_user.bio = update_data.bio
    if update_data.phone_number is not None:
        current_user.phone_number = update_data.phone_number
    if update_data.email is not None:
        current_user.email = update_data.email

    db.commit()
    db.refresh(current_user)

    return UserProfile(
        user_id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        bio=current_user.bio,
        phone_number=current_user.phone_number,
        profile_picture=current_user.profile_picture,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@User_rotues.put("/Update_Picture", response_model=UpdateProfilePictureResponse)
async def Update_Picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload and update the authenticated user's profile picture.
    Accepts: image/jpeg, image/png, image/webp (max 5 MB).
    """
    ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
    MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

    if file.content_type not in ALLOWED_TYPES:
        raise UnsupportedMediaType()


    # Read file and enforce size limit
    contents = await file.read()
    if len(contents) > MAX_SIZE_BYTES:
        raise RequestEntityTooLarge()


    # Delete old picture file from disk if it exists
    if current_user.profile_picture:
        old_path = current_user.profile_picture.lstrip("/")
        if os.path.isfile(old_path):
            os.remove(old_path)

    # Build a unique filename to avoid collisions
    extension = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg"
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Write to disk
    with open(file_path, "wb") as f:
        f.write(contents)

    # Persist the relative URL in the DB
    picture_url = f"/{file_path.replace(os.sep, '/')}"
    current_user.profile_picture = picture_url

    db.commit()
    db.refresh(current_user)

    return UpdateProfilePictureResponse(
        message=f"Profile picture updated successfully. URL: {picture_url}"
    )


@User_rotues.delete("/Delete_Profile", status_code=status.HTTP_200_OK)
async def Delete_Profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Permanently delete the authenticated user's account."""
    db.delete(current_user)
    db.commit()
    return {"message": "User account deleted successfully"}


@User_rotues.put("/grant-admin")
async def grant_admin(
    data: GrantAdminRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Admin-only: grant `is_admin=True` to another user."""
    # Use get_current_user as requested; perform the admin check on the fetched user.
    if not current_user.is_admin:
        raise Forbidden()


    target = db.query(User).filter(User.id == data.user_id).first()
    if not target:
        raise NotFound()


    if target.is_admin:
        return {"message": "User is already an admin", "user_id": target.id}

    target.is_admin = True
    db.commit()
    db.refresh(target)

    return {"message": "Admin privileges granted", "user_id": target.id, "is_admin": target.is_admin}


@User_rotues.get("/Profile/{user_id}", response_model=UserProfile)
async def Get_User_Profile_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get a public profile by user ID (no auth required)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFound()

    return UserProfile(
        user_id=user.id,
        username=user.username,
        email=user.email,
        bio=user.bio,
        phone_number=user.phone_number,
        profile_picture=user.profile_picture,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

