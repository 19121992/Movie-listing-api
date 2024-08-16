from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    
    # Ensure that rating_value is non-nullable and has some application-level validation
    rating_value = Column(Integer, nullable=False)  
    
    # Indexes on foreign keys for better query performance
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Establishing relationships with back_populates to the associated Movie and User models
    movie = relationship("Movie", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
