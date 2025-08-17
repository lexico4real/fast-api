from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from configs.database import get_db
from schemas.user import UserCreate, UserOut
from services.user_service import UserService
from configs.exceptions import UserAlreadyExistsError, UserNotFoundError
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService.create_user(db, data)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    try:
        return UserService.get_user(db, user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[UserOut])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return UserService.list_users(db, skip=skip, limit=limit)


@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        UserService.delete_user(db, user_id)
        return {"message": "User deleted"}
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
