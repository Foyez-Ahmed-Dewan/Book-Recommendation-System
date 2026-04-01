from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class RecommendationRequest(BaseModel):
    query: Optional[str] = Field(default=None)
    top_k: int = Field(default=10, ge=1, le=40)

    genre: Optional[str] = None
    author: Optional[str] = None
    min_rating: Optional[float] = Field(default=None, ge=0, le=5)

    @field_validator("query", "genre", "author", mode="before")
    @classmethod
    def strip_string_fields(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            value = value.strip()
            return value if value else None
        return value


class BookResponse(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    rating: Optional[float] = None
    totalratings: Optional[int] = None
    weighted_score: Optional[float] = None
    img: Optional[str] = None


class RecommendationResponse(BaseModel):
    message: str
    count: int
    results: List[BookResponse]