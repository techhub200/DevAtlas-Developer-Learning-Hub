from pydantic import BaseModel, Field
from datetime import datetime

# ── Input schemas ────────────────────────────────────────────────────────────

class CourseCreate(BaseModel):
    """Payload for creating a new course."""
    title: str = Field(..., max_length=255, examples=["Advanced Python Course"])
    description: str | None = Field(default=None, examples=["A comprehensive guide to advanced Python topics."])
    technology_name: str = Field(..., max_length=100, examples=["Python"])


class CourseUpdate(BaseModel):
    """Payload for updating an existing course."""
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    technology_name: str | None = Field(default=None, max_length=100)


# ── Output schemas ───────────────────────────────────────────────────────────

class CourseResponse(BaseModel):
    """Full course record returned from the API."""
    id: int
    title: str
    description: str | None
    technology_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CourseListResponse(BaseModel):
    """Paginated list wrapper."""
    total: int
    items: list[CourseResponse]
