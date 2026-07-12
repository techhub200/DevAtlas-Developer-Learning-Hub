from pydantic import BaseModel, Field
from datetime import datetime


# ── Input schemas (request bodies) ──────────────────────────────────────────

class TechnologyCreate(BaseModel):
    """Payload for creating a new technology."""
    name: str = Field(..., max_length=100, examples=["Python"])
    category: str = Field(..., max_length=100, examples=["Programming Language"])
    about: str | None = Field(default=None, examples=["A high-level, general-purpose programming language."])


class TechnologyUpdate(BaseModel):
    """Payload for updating an existing technology (all fields optional)."""
    name: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=100)
    about: str | None = None


# ── Output schemas (response models) ────────────────────────────────────────

class TechnologyResponse(BaseModel):
    """Full technology record returned from the API."""
    id: int
    name: str
    category: str
    created_by: int | None   # user_id of the creator (None if user was deleted)
    about: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TechnologyListResponse(BaseModel):
    """Paginated list wrapper."""
    total: int
    items: list[TechnologyResponse]
