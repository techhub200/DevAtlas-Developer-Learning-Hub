from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.schemas import Technology
from src.api.technologies.schemas import TechnologyCreate, TechnologyUpdate


class TechnologyService:

    # ── Create ───────────────────────────────────────────────────────────────

    def create_technology(
        self,
        data: TechnologyCreate,
        created_by: int,
        db: Session,
    ) -> Technology:
        
        existing = db.query(Technology).filter(Technology.name == data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Technology '{data.name}' already exists.",
            )

        technology = Technology(
            name=data.name,
            category=data.category,
            about=data.about,
            created_by=created_by,
        )
        db.add(technology)
        db.commit()
        db.refresh(technology)
        return technology

    # ── Read (single) ────────────────────────────────────────────────────────

    def get_technology_by_name(self, name: str, db: Session) -> Technology:
        """Fetch a single technology by its unique name (case-insensitive). Raises 404 if not found."""
        technology = db.query(Technology).filter(Technology.name.ilike(name)).first()
        if not technology:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Technology '{name}' not found.",
            )
        return technology

    # ── Read (list) ──────────────────────────────────────────────────────────

    def get_all_technologies(
        self,
        db: Session,
        category: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[int, list[Technology]]:
        """
        Return a paginated list of technologies.

        Args:
            db:       Database session.
            category: Optional filter by category (case-insensitive).
            skip:     Number of records to skip (offset).
            limit:    Maximum number of records to return.

        Returns:
            A tuple of (total_count, items).
        """
        query = db.query(Technology)

        if category:
            query = query.filter(Technology.category.ilike(f"%{category}%"))

        total = query.count()
        items = query.order_by(Technology.created_at.desc()).offset(skip).limit(limit).all()
        return total, items

    # ── Update ───────────────────────────────────────────────────────────────

    def update_technology(
        self,
        name: str,
        data: TechnologyUpdate,
        db: Session,
    ) -> Technology:
        """Update an existing technology by name. Raises 404 if not found, 409 on name conflict."""
        technology = self.get_technology_by_name(name, db)

        # Check name uniqueness if a new name is being set
        if data.name and data.name != technology.name:
            conflict = db.query(Technology).filter(Technology.name == data.name).first()
            if conflict:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Technology '{data.name}' already exists.",
                )

        if data.name is not None:
            technology.name = data.name
        if data.category is not None:
            technology.category = data.category
        if data.about is not None:
            technology.about = data.about

        db.commit()
        db.refresh(technology)
        return technology

    # ── Delete ───────────────────────────────────────────────────────────────

    def delete_technology(self, name: str, db: Session) -> None:
        """Permanently delete a technology by name. Raises 404 if not found."""
        technology = self.get_technology_by_name(name, db)
        db.delete(technology)
        db.commit()


# Module-level singleton — import this in routes
technology_service = TechnologyService()
