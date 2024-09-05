from fastapi import FastAPI, Request
from app.routers import auth, movie, rating, comment
from app.database import Base, engine

app = FastAPI()

@app.middleware("http")
async def get_real_ip(request: Request, call_next):
    real_ip = request.headers.get("x-forwarded-for", "").split(",")[0]
    request.state.ip = real_ip  # Now you can use `request.state.ip` wherever you need the client's real IP
    response = await call_next(request)
    return response

# Include your routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(movie.router, prefix="/movies", tags=["movies"])
app.include_router(rating.router, prefix="/ratings", tags=["ratings"])
app.include_router(comment.router, prefix="/comments", tags=["comments"])

# Initialize database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Listing App"}
