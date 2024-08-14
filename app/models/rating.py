from sqlalchemy import Column, Integer, ForeignKey 
from sqlalchemy.orm import relationship
from app.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    movie = relationship("Movie", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
