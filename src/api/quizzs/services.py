from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.schemas import Quiz, Course
from src.api.quizzs.schemas import QuizCreate, QuizUpdate


class QuizService:
    """Service layer for Quiz CRUD operations."""

    # ── Create ────────────────────────────────────────────────────────────────

    def create_quiz(
        self,
        data: QuizCreate,
        db: Session,
    ) -> Quiz:
        """Create a new quiz. Validates that the course exists and no duplicate title within that course."""
        # Validate course exists
        course = db.query(Course).filter(Course.id == data.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with id '{data.course_id}' not found.",
            )

        # Check for duplicate title in the same course
        existing = (
            db.query(Quiz)
            .filter(Quiz.course_id == data.course_id, Quiz.title == data.title)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Quiz '{data.title}' already exists in course id '{data.course_id}'.",
            )

        quiz = Quiz(
            course_id=data.course_id,
            title=data.title,
            description=data.description,
        )
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        return quiz

    # ── Read (list) ──────────────────────────────────────────────────────────

    def get_quizzes(
        self,
        db: Session,
        course_id: int | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[int, list[Quiz]]:
        """Return a paginated list of quizzes. Optional filter by course_id."""
        query = db.query(Quiz)

        if course_id is not None:
            query = query.filter(Quiz.course_id == course_id)

        total = query.count()
        items = query.order_by(Quiz.created_at.desc()).offset(skip).limit(limit).all()
        return total, items

    # ── Read (single) ────────────────────────────────────────────────────────

    def get_quiz_by_id(self, quiz_id: int, db: Session) -> Quiz:
        """Fetch a single quiz by its ID. Raises 404 if not found."""
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quiz with id '{quiz_id}' not found.",
            )
        return quiz

    # ── Update ───────────────────────────────────────────────────────────────

    def update_quiz(
        self,
        quiz_id: int,
        data: QuizUpdate,
        db: Session,
    ) -> Quiz:
        """Update an existing quiz by ID. Raises 404 if not found, 409 on title conflict."""
        quiz = self.get_quiz_by_id(quiz_id, db)

        # If title is being changed, check for duplicates within the same course
        if data.title is not None and data.title != quiz.title:
            conflict = (
                db.query(Quiz)
                .filter(Quiz.course_id == quiz.course_id, Quiz.title == data.title)
                .first()
            )
            if conflict:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Quiz '{data.title}' already exists in this course.",
                )
            quiz.title = data.title

        if data.description is not None:
            quiz.description = data.description

        db.commit()
        db.refresh(quiz)
        return quiz

    # ── Delete ───────────────────────────────────────────────────────────────

    def delete_quiz(self, quiz_id: int, db: Session) -> None:
        """Permanently delete a quiz by ID. Raises 404 if not found."""
        quiz = self.get_quiz_by_id(quiz_id, db)
        db.delete(quiz)
        db.commit()


# Module-level singleton
quiz_service = QuizService()

