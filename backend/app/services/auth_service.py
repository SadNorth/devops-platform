from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session


class AuthService:

    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: UserCreate):

        if self.repo.get_by_email(data.email):
            raise ValueError("User alreay exists")
        
        if self.repo.get_by_username(data.username):
            raise ValueError("Username already exists")
        
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
        )

        return self.repo.create(user)