from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.database.sessions import get_db
from src.database.schemas import User
from src.api.auth.dpendencies import get_current_user, require_admin
from src.api.course.schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseListResponse,
)
from src.api.course.services import course_service

course_router = APIRouter()


# ── 1. POST create course (admin only) ───────────────────────────────────────

@course_router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new course (admin only)",
)
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin), # Admin specific operation
):
    """
    Admin-only endpoint.
    Creates a new course related to an existing technology.
    """
    return course_service.create_course(data, db=db)


# ── 2. GET all courses ───────────────────────────────────────────────────────

@course_router.get(
    "/",
    response_model=CourseListResponse,
    summary="List all courses",
)
def get_all_courses(
    technology_name: str | None = Query(default=None, description="Filter by technology name (partial, case-insensitive)"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """
    Public endpoint.
    Returns a paginated list of all courses.
    Optionally filter by `technology_name`.
    """
    total, items = course_service.get_courses(db, technology_name=technology_name, skip=skip, limit=limit)
    return CourseListResponse(total=total, items=items)


# ── 3. GET course by name (title) ────────────────────────────────────────────

@course_router.get(
    "/{title}",
    response_model=CourseResponse,
    summary="Get a course by title",
)
def get_course_by_name(
    title: str,
    db: Session = Depends(get_db),
):
    """
    Public endpoint.
    Lookup is case-insensitive.
    """
    return course_service.get_course_by_name(title, db)


# ── 4. PATCH update course (admin only) ──────────────────────────────────────

@course_router.patch(
    "/{title}",
    response_model=CourseResponse,
    summary="Update a course by title (admin only)",
)
def update_course(
    title: str,
    data: CourseUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin), # Admin specific operation
):
    """
    Admin-only endpoint.
    Only fields that are provided (non-None) will be updated.
    """
    return course_service.update_course(title, data, db)


# ── 5. DELETE course (admin only) ────────────────────────────────────────────

@course_router.delete(
    "/{title}",
    status_code=status.HTTP_200_OK,
    summary="Delete a course by title (admin only)",
)
def delete_course(
    title: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin), # Admin specific operation
):
    """
    Admin-only endpoint.
    Permanently deletes a course record.
    """
    course_service.delete_course(title, db)
    return {"message": f"Course '{title}' deleted successfully."}
