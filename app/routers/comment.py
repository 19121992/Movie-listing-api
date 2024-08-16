from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.comment import Comment, CommentCreate
from app.models.comment import Comment as CommentModel
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

@router.post("/", response_model=Comment)
def create_comment(comment: CommentCreate, movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_comment = CommentModel(**comment.dict(), movie_id=movie_id, user_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/movie/{movie_id}", response_model=List[Comment])
def read_comments_for_movie(movie_id: int, db: Session = Depends(get_db)):
    comments = db.query(CommentModel).filter(CommentModel.movie_id == movie_id).all()
    return comments

@router.get("/{comment_id}", response_model=Comment)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment
