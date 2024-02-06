from pydantic import BaseModel, Field
from config.database import Base
from sqlalchemy import Column, Float, Integer, String


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    category = Column(String)
    rating = Column(Float)


class MovieJson(BaseModel):
    id: int | None = None
    title: str = Field(min_length=5, max_length=15)
    overview: str | None = None
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le=10)
    category: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 0,
                    "title": "Movie",
                    "overview": "Best movie ever",
                    "year": 2002,
                    "rating": 0.0,
                    "category": "Movie"
                }
            ]
        }
    }
