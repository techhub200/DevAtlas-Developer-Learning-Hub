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

    @staticmethod
    def from_orm_with_technology(course) -> "CourseResponse":
        """Build response from a Course ORM object, resolving technology_name from the relationship."""
        return CourseResponse(
            id=course.id,
            title=course.title,
            description=course.description,
            technology_name=course.technology.name if course.technology else "Unknown",
            created_at=course.created_at,
            updated_at=course.updated_at,
        )


class CourseListResponse(BaseModel):
    """Paginated list wrapper."""
    total: int
    items: list[CourseResponse]
