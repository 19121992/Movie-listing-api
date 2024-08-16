from pydantic import BaseModel
from typing import Optional

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None  # Make description optional here

class MovieCreate(MovieBase):
    director: str
    release_year: int
    genre: str

class Movie(MovieBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
