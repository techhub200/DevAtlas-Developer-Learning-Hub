from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey
from sqlalchemy import String, Text, DateTime
from datetime import datetime
from sqlalchemy import UniqueConstraint


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    username: Mapped[str] = mapped_column(

        String(50),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password: Mapped[str] = mapped_column(
        String(72),
        nullable=False
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    profile_picture: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    is_admin: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        server_default="0",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    technologies: Mapped[list["Technology"]] = relationship(
        back_populates="created_by_user",
        cascade="all, delete-orphan",
    )

    bookmarks: Mapped[list["Bookmark"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )



class Technology(Base):
    __tablename__ = "technologies"


    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # FK to the user who created this technology entry
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    about: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    created_by_user: Mapped["User"] = relationship(
        "User",
        back_populates="technologies",
    )



    courses: Mapped[list["Course"]] = relationship(
        back_populates="technology",
        cascade="all, delete-orphan",
    )


class Course(Base):
    __tablename__ = "courses"


    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    technology_id: Mapped[int] = mapped_column(
        ForeignKey("technologies.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    technology: Mapped["Technology"] = relationship(
        back_populates="courses",
    )

    quizzes: Mapped[list["Quiz"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )

    bookmarks: Mapped[list["Bookmark"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )



class Recommendation(Base):

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    resource_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Expected values:
    # Technology, Course, Article, Video, GitHub Repository
    resource_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )



class Quiz(Base):
    __tablename__ = "quizzes"


    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    course: Mapped["Course"] = relationship(
        "Course",
        back_populates="quizzes",
    )


class Bookmark(Base):

    __tablename__ = "bookmarks"


    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(

        "User",
        back_populates="bookmarks",
    )

    course: Mapped["Course"] = relationship(
        "Course",
        back_populates="bookmarks",
    )

    __tablename__ = "bookmarks"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "course_id",
            name="uq_user_course_bookmark",
        ),
    )


