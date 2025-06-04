from pydantic import BaseModel, Field
from typing import Optional

class Album(BaseModel):
    id: Optional[int] | None # Indicamos que es opcional
    title: str = Field(min_length=5, max_length=15)
    artist: str = Field(max_length=30)
    overview: str = Field(min_length=5, max_length=40)
    year: int = Field(le=2025)
    rating: float = Field(ge=1, le=10)
    genre: str = Field(min_length=5, max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi album",
                "artist": "Interprete",
                "overview": "Descripción",
                "year": 2025,
                "rating": 9.9,
                "genre": "Alternative"
            }
        }