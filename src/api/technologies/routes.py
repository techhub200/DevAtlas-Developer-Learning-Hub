from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.database.sessions import get_db
from src.database.schemas import User
from src.api.auth.dependencies import get_current_user, require_admin
from src.api.technologies.schemas import (
    TechnologyCreate,
    TechnologyUpdate,
    TechnologyResponse,
    TechnologyListResponse,
)
from src.api.technologies.service import technology_service

tech_router = APIRouter()


# ── 1. GET all technologies ──────────────────────────────────────────────────

@tech_router.get(
    "/",
    response_model=TechnologyListResponse,
    summary="List all technologies",
)
def get_all_technologies(
    category: str | None = Query(default=None, description="Filter by category (partial, case-insensitive)"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """
    Public endpoint — no auth required.
    Returns a paginated list of all technologies.
    Optionally filter by `category`.
    """
    total, items = technology_service.get_all_technologies(db, category=category, skip=skip, limit=limit)
    return TechnologyListResponse(total=total, items=items)


# ── 2. GET technology by name ────────────────────────────────────────────────

@tech_router.get(
    "/{name}",
    response_model=TechnologyResponse,
    summary="Get a technology by name",
)
def get_technology_by_name(
    name: str,
    db: Session = Depends(get_db),
):
    """
    Public endpoint — no auth required.
    Lookup is case-insensitive, so 'python' and 'Python' resolve to the same record.
    """
    return technology_service.get_technology_by_name(name, db)


# ── 3. POST create technology (authenticated) ────────────────────────────────

@tech_router.post(
    "/",
    response_model=TechnologyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new technology",
)
def create_technology(
    data: TechnologyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Authenticated endpoint.
    The `created_by` field is automatically set to the logged-in user's ID.
    """
    return technology_service.create_technology(data, created_by=current_user.id, db=db)


# ── 4. PATCH update technology (authenticated) ───────────────────────────────

@tech_router.patch(
    "/{name}",
    response_model=TechnologyResponse,
    summary="Update a technology by name",
)
def update_technology(
    name: str,
    data: TechnologyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Authenticated endpoint.
    Only fields that are provided (non-None) will be updated.
    """
    return technology_service.update_technology(name, data, db)


# ── 5. DELETE technology (admin only) ────────────────────────────────────────

@tech_router.delete(
    "/{name}",
    status_code=status.HTTP_200_OK,
    summary="Delete a technology by name (admin only)",
)
def delete_technology(
    name: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),   # underscore — we only need the auth check
):
    """
    Admin-only endpoint.
    Permanently deletes a technology record. Returns 403 for non-admins.
    """
    technology_service.delete_technology(name, db)
    return {"message": f"Technology '{name}' deleted successfully."}
