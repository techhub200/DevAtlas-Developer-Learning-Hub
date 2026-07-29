from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.api.auth.dependencies import require_admin
from src.api.recommendations.schemas import (
    RecommendationCreate,
    RecommendationListResponse,
    RecommendationResponse,
)
from src.api.recommendations.service import recommendation_service
from src.database.sessions import get_db
from src.database.schemas import User


recommendations_router = APIRouter()


@recommendations_router.get(
    "/",
    response_model=RecommendationListResponse,
    summary="List recommendations",
)
def get_recommendations(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    total, items = recommendation_service.get_recommendations(db, skip=skip, limit=limit)
    return RecommendationListResponse(total=total, items=items)


@recommendations_router.post(
    "/",
    response_model=RecommendationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a recommendation (admin only)",
)
def create_recommendation(
    data: RecommendationCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return recommendation_service.create_recommendation(data, db=db)


@recommendations_router.delete(
    "/{recommendation_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a recommendation by id (admin only)",
)
def delete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    recommendation_service.delete_recommendation(recommendation_id, db=db)
    return {"message": f"Recommendation {recommendation_id} deleted successfully."}

