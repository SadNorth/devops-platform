from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

# from app.db.session import engine
from app.api.auth import router as auth_router
from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

app = FastAPI(
    title="DevOps Platform API",
    version="1.0.0"
)

@app.get("/")

# async def root():
#    return {
#        "status": "running",
#        "service": "backend"
#    }

def root(db: Session = Depends(get_db)):
    version = db.execute(text("SELECT version()")).scalar()

    return {
        "status": "running",
        "database": version,
    }

app.include_router(auth_router)

@app.get("/me")
def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }