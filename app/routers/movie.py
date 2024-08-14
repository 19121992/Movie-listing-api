from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from typing import List
from app.schemas.movie import Movie, MovieCreate
from app.models.movie import Movie as MovieModel
from app.database import SessionLocal
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Movie)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_movie = MovieModel(**movie.dict(), owner_id=current_user.id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/", response_model=List[Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = db.query(MovieModel).offset(skip).limit(limit).all()
    return movies

@router.get("/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie 
from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from typing import List
from app.schemas.movie import Movie, MovieCreate
from app.models.movie import Movie as MovieModel
from app.database import SessionLocal
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Movie)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_movie = MovieModel(**movie.dict(), owner_id=current_user.id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/", response_model=List[Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = db.query(MovieModel).offset(skip).limit(limit).all()
    return movies

@router.get("/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie 