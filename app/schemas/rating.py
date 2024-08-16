from pydantic import BaseModel 

class RatingBase(BaseModel):
    rating: int

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    movie_id: int
    user_id: int

    class Config:
        orm_mode = True