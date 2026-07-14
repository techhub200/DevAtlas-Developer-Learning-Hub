from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.api.recommendations.schemas import RecommendationCreate
from src.database.schemas import Recommendation


class RecommendationService:
    def create_recommendation(
        self,
        data: RecommendationCreate,
        db: Session,
    ) -> Recommendation:
        recommendation = Recommendation(
            description=data.description,
            resource_url=data.resource_url,
            resource_type=data.resource_type.value,
        )
        db.add(recommendation)
        db.commit()
        db.refresh(recommendation)
        return recommendation

    def get_recommendations(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[int, list[Recommendation]]:
        query = db.query(Recommendation)
        total = query.count()
        items = (
            query.order_by(Recommendation.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return total, items

    def delete_recommendation(self, recommendation_id: int, db: Session) -> None:
        recommendation = (
            db.query(Recommendation)
            .filter(Recommendation.id == recommendation_id)
            .first()
        )
        if not recommendation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recommendation with id {recommendation_id} not found.",
            )

        db.delete(recommendation)
        db.commit()


# Module-level singleton
recommendation_service = RecommendationService()

