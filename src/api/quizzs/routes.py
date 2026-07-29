from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.database.sessions import get_db
from src.database.schemas import User
from src.api.auth.dependencies import get_current_user, require_admin
from src.api.quizzs.schemas import (
    QuizCreate,
    QuizUpdate,
    QuizResponse,
    QuizListResponse,
)
from src.api.quizzs.services import quiz_service

quizz_router = APIRouter()


# ── 1. POST create quiz (admin only) ─────────────────────────────────────────

@quizz_router.post(
    "/",
    response_model=QuizResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new quiz (admin only)",
)
def create_quiz(
    data: QuizCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Admin-only endpoint.
    Creates a new quiz linked to an existing course.
    """
    return quiz_service.create_quiz(data, db=db)


# ── 2. GET all quizzes ───────────────────────────────────────────────────────

@quizz_router.get(
    "/",
    response_model=QuizListResponse,
    summary="List all quizzes",
)
def get_all_quizzes(
    course_id: int | None = Query(default=None, description="Filter by course ID"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """
    Public endpoint.
    Returns a paginated list of all quizzes.
    Optionally filter by `course_id`.
    """
    total, items = quiz_service.get_quizzes(db, course_id=course_id, skip=skip, limit=limit)
    return QuizListResponse(total=total, items=items)


# ── 3. GET quiz by ID ────────────────────────────────────────────────────────

@quizz_router.get(
    "/{quiz_id}",
    response_model=QuizResponse,
    summary="Get a quiz by ID",
)
def get_quiz_by_id(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    """
    Public endpoint.
    Fetches a single quiz by its primary key ID.
    """
    return quiz_service.get_quiz_by_id(quiz_id, db)


# ── 4. PATCH update quiz (admin only) ────────────────────────────────────────

@quizz_router.patch(
    "/{quiz_id}",
    response_model=QuizResponse,
    summary="Update a quiz by ID (admin only)",
)
def update_quiz(
    quiz_id: int,
    data: QuizUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Admin-only endpoint.
    Only fields that are provided (non-None) will be updated.
    """
    return quiz_service.update_quiz(quiz_id, data, db)


# ── 5. DELETE quiz (admin only) ──────────────────────────────────────────────

@quizz_router.delete(
    "/{quiz_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a quiz by ID (admin only)",
)
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Admin-only endpoint.
    Permanently deletes a quiz record.
    """
    quiz_service.delete_quiz(quiz_id, db)
    return {"message": f"Quiz with id '{quiz_id}' deleted successfully."}

