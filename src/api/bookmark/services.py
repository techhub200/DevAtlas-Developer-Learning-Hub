from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.schemas import Bookmark, Course, Technology
from src.api.bookmark.schemas import BookmarkResponse


class Bookmark_Services:

    def get_all_bookmarks(self, current_user, db: Session):
        bookmarked_courses = (
            db.query(Bookmark, Course, Technology)
            .join(Course, Bookmark.course_id == Course.id)
            .join(Technology, Course.technology_id == Technology.id)
            .filter(Bookmark.user_id == current_user.id)
            .all()
        )

        items = [
            BookmarkResponse(
                id=bookmark.id,
                course_id=course.id,
                course_title=course.title,
                course_description=course.description,
                technology_name=technology.name,
                bookmarked_at=bookmark.created_at,
            )
            for bookmark, course, technology in bookmarked_courses
        ]

        return {"total": len(items), "items": items}

    def create_bookmark(self, course_id: int, current_user, db: Session):
        existing = db.query(Bookmark).filter(
            Bookmark.user_id == current_user.id,
            Bookmark.course_id == course_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bookmark already exists"
            )

        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )

        new_bookmark = Bookmark(user_id=current_user.id, course_id=course_id)
        db.add(new_bookmark)
        db.commit()
        db.refresh(new_bookmark)

        return {"message": "Bookmark created successfully", "id": new_bookmark.id}

    def delete_bookmark(self, course_id: int, current_user, db: Session):
        bookmark = db.query(Bookmark).filter(
            Bookmark.user_id == current_user.id,
            Bookmark.course_id == course_id
        ).first()

        if not bookmark:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bookmark not found"
            )

        db.delete(bookmark)
        db.commit()

        return {"message": "Bookmark deleted successfully"}
   