from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.schemas import Course, Technology
from src.api.course.schemas import CourseCreate, CourseUpdate


class CourseService:
    

    def create_course(
        self,
        data: CourseCreate,
        db: Session,
    ) -> Course:
       
        # Validate that the technology actually exists
        tech = db.query(Technology).filter(Technology.name == data.technology_name).first()
        if not tech:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Technology '{data.technology_name}' not found. Cannot create course.",
            )

        existing = db.query(Course).filter(Course.title == data.title).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Course '{data.title}' already exists.",
            )

        course = Course(
            title=data.title,
            description=data.description,
            
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    # ── Read (list) ──────────────────────────────────────────────────────────

    def get_courses(
        self,
        db: Session,
        technology_name: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[int, list[Course]]:
        """Return a paginated list of courses. Optional filter by technology name."""
        query = db.query(Course)

        if technology_name:
            query = query.filter(Course.technology_name.ilike(f"%{technology_name}%"))

        total = query.count()
        items = query.order_by(Course.created_at.desc()).offset(skip).limit(limit).all()
        return total, items

    # ── Read (single) ────────────────────────────────────────────────────────

    def get_course_by_name(self, title: str, db: Session) -> Course:
        """Fetch a single course by its unique title. Raises 404 if not found."""
        course = db.query(Course).filter(Course.title.ilike(title)).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course '{title}' not found.",
            )
        return course

    # ── Update ───────────────────────────────────────────────────────────────

    def update_course(
        self,
        title: str,
        data: CourseUpdate,
        db: Session,
    ) -> Course:
        """Update an existing course by title. Raises 404 if not found, 409 on conflict."""
        course = self.get_course_by_name(title, db)

        if data.title and data.title != course.title:
            conflict = db.query(Course).filter(Course.title == data.title).first()
            if conflict:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Course '{data.title}' already exists.",
                )
        
        if data.technology_name and data.technology_name != course.technology_name:
            tech = db.query(Technology).filter(Technology.name == data.technology_name).first()
            if not tech:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Technology '{data.technology_name}' not found.",
                )
            course.technology_name = tech.name

        if data.title is not None:
            course.title = data.title
        if data.description is not None:
            course.description = data.description

        db.commit()
        db.refresh(course)
        return course

    # ── Delete ───────────────────────────────────────────────────────────────

    def delete_course(self, title: str, db: Session) -> None:
        """Permanently delete a course by title. Raises 404 if not found."""
        course = self.get_course_by_name(title, db)
        db.delete(course)
        db.commit()


# Module-level singleton
course_service = CourseService()
