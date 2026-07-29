from pydantic import BaseModel, Field
from datetime import datetime


# ── Input schemas ────────────────────────────────────────────────────────────

class QuizCreate(BaseModel):
    """Payload for creating a new quiz."""
    course_id: int = Field(..., description="ID of the course this quiz belongs to")
    title: str = Field(..., max_length=255, examples=["Python Basics Quiz"])
    description: str | None = Field(default=None, examples=["Test your knowledge on Python basics."])


class QuizUpdate(BaseModel):
    """Payload for updating an existing quiz."""
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None


# ── Output schemas ───────────────────────────────────────────────────────────

class QuizResponse(BaseModel):
    """Full quiz record returned from the API."""
    id: int
    course_id: int
    title: str
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class QuizListResponse(BaseModel):
    """Paginated list wrapper."""
    total: int
    items: list[QuizResponse]

