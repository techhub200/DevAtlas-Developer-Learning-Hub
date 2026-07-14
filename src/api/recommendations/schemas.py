from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    Technology = "Technology"
    Course = "Course"
    Article = "Article"
    Video = "Video"
    GitHub_Repository = "GitHub Repository"



class RecommendationCreate(BaseModel):
    description: str = Field(..., min_length=1)
    resource_url: str = Field(..., min_length=1, examples=["https://example.com"])
    resource_type: ResourceType


class RecommendationResponse(BaseModel):
    id: int
    description: str
    resource_url: str
    resource_type: ResourceType
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RecommendationListResponse(BaseModel):
    total: int
    items: list[RecommendationResponse]

