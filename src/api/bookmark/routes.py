from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.sessions import get_db
from src.database.schemas import User
from src.api.auth.dependencies import get_current_user, require_admin
from src.api.bookmark.schemas import BookmarkListResponse, add_bookmark, delete_bookmarks
from src.api.bookmark.services import Bookmark_Services

bookmark_route = APIRouter()


@bookmark_route.get("/my_bookmark", response_model=BookmarkListResponse)
async def my_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    service = Bookmark_Services()
    return service.get_all_bookmarks(current_user=current_user, db=db)


@bookmark_route.post("/create_bookmark")
async def make_bookmarks(
    request: add_bookmark,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = Bookmark_Services()
    return service.create_bookmark(
        course_id=request.course_id,
        current_user=current_user,
        db=db
    )


@bookmark_route.delete("/delete_bookmark")
async def delete_bookmarks(
    request: delete_bookmarks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = Bookmark_Services()
    return service.delete_bookmark(
        course_id=request.course_id,
        current_user=current_user,
        db=db
    )
