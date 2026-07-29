from pydantic import BaseModel, Field
from datetime import datetime


class add_bookmark(BaseModel):
    course_id: int


class BookmarkResponse(BaseModel):
    id: int
    course_id: int
    course_title: str
    course_description: str | None
    technology_name: str
    bookmarked_at: datetime

    model_config = {"from_attributes": True}


class BookmarkListResponse(BaseModel):
   
    total: int
    items: list[BookmarkResponse]


class delete_bookmars(BaseModel):
    course_id: int

