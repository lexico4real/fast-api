from typing import List
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from schemas.user import UserCreate
from models.user import User
from configs.exceptions import UserAlreadyExistsError, UserNotFoundError


class UserService:
    @staticmethod
    def create_user(db: Session, data: UserCreate) -> User:
        if UserRepository.get_by_email(db, data.email):
            raise UserAlreadyExistsError("Email already registered")
        return UserRepository.create(db, data)

    @staticmethod
    def get_user(db: Session, user_id: str) -> User:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError("User not found")
        return user

    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
        return UserRepository.list(db, skip=skip, limit=limit)

    @staticmethod
    def delete_user(db: Session, user_id: str) -> None:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError("User not found")
        UserRepository.delete(db, user)
