from app.core.jwt import create_access_token
from app.core.security import pwd_context
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])

# pwd_context = CryptContext(
#    schemes=["bcrypt"],
#    deprecated="auto"
# )

@router.post(
    "/login",
    response_model=TokenResponse
)

def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    if not pwd_context.verify(
        data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    token = create_access_token({
        "sub": str(user.id)
    })

    return TokenResponse(
        access_token=token,
        token_type="bearer"
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)

def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.register(user)
    
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e) 
        )