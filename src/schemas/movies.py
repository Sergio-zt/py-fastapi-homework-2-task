from datetime import date, timedelta
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from database.models import MovieStatusEnum


# ---------------------------------------------------------------------------
# Related-entity schemas
# ---------------------------------------------------------------------------

class CountrySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: Optional[str] = None


class GenreSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ActorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class LanguageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


# ---------------------------------------------------------------------------
# Movie list (GET /movies/)
# ---------------------------------------------------------------------------

class MovieListItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    date: date
    score: float
    overview: str


class MovieListResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    movies: List[MovieListItemSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int


# ---------------------------------------------------------------------------
# Movie detail (GET /movies/{id}/, POST /movies/)
# ---------------------------------------------------------------------------

class MovieDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    date: date
    score: float
    overview: str
    status: MovieStatusEnum
    budget: float
    revenue: float
    country: CountrySchema
    genres: List[GenreSchema]
    actors: List[ActorSchema]
    languages: List[LanguageSchema]


# ---------------------------------------------------------------------------
# Validators shared between create / update
# ---------------------------------------------------------------------------

def _validate_not_too_far_in_future(value: Optional[date]) -> Optional[date]:
    if value is None:
        return value
    max_allowed_date = date.today() + timedelta(days=365)
    if value > max_allowed_date:
        raise ValueError("Date must not be more than one year in the future.")
    return value


# ---------------------------------------------------------------------------
# Movie creation (POST /movies/)
# ---------------------------------------------------------------------------

class MovieCreateSchema(BaseModel):
    name: str = Field(..., max_length=255)
    date: date
    score: float = Field(..., ge=0, le=100)
    overview: str
    status: MovieStatusEnum
    budget: float = Field(..., ge=0)
    revenue: float = Field(..., ge=0)
    country: str = Field(..., min_length=1, max_length=3)
    genres: List[str] = Field(default_factory=list)
    actors: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: date) -> date:
        return _validate_not_too_far_in_future(value)


# ---------------------------------------------------------------------------
# Movie update (PATCH /movies/{id}/)
# ---------------------------------------------------------------------------

class MovieUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    date: Optional[date] = None
    score: Optional[float] = Field(default=None, ge=0, le=100)
    overview: Optional[str] = None
    status: Optional[MovieStatusEnum] = None
    budget: Optional[float] = Field(default=None, ge=0)
    revenue: Optional[float] = Field(default=None, ge=0)

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: Optional[date]) -> Optional[date]:
        return _validate_not_too_far_in_future(value)


class MessageResponseSchema(BaseModel):
    detail: str
