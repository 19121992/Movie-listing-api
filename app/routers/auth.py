from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate
from app.models.user import User as UserModel
from app.utils.security import get_password_hash, create_access_token, verify_password
from app.database import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User registration endpoint
@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user with the given email already exists
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    # If a user with this email already exists, raise an error
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the user's password
    hashed_password = get_password_hash(user.password)

    # Create a new user instance
    db_user = UserModel(username=user.username, email=user.email, hashed_password=hashed_password)

    # Add the new user to the database and commit the transaction
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh the instance to get the generated ID

    # Return the newly created user
    return db_user

# Pydantic model for login request
class UserLoginRequest(BaseModel):
    email: str
    password: str

# User login endpoint
@router.post("/login")
def login(user: UserLoginRequest, db: Session = Depends(get_db)):
    # Fetch the user by email
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    # Verify if the user exists and the password is correct
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Create an access token for the user
    access_token = create_access_token(data={"sub": db_user.email})

    # Return the access token
    return {"access_token": access_token, "token_type": "bearer"}
