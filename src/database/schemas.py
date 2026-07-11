from sqlalchemy.orm import declarative_base,Mapped,mapped_column
from sqlalchemy import func
from sqlalchemy import String, Text, DateTime
from datetime import datetime



Base=declarative_base()

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
        String(255),
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