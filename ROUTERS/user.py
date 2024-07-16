from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List

from schemas import UserDisplay, UserBase
from DB.database import get_db
from DB import db_user
from DB.models import User
from AUTH.oauth2 import get_current_user

db_dependency = Depends(get_db)

router = APIRouter(prefix='/user', tags=['user'])

@router.post("/create/", response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = db_dependency):
    return db_user.create_user(user, db)
    
@router.get("/get/all/", status_code=status.HTTP_200_OK, response_model=List[UserDisplay])
async def read_users(db: Session = db_dependency):
    return db_user.get_all_users(db)

@router.get("/get/by_id/{user_id}/", status_code=status.HTTP_200_OK, response_model=UserDisplay)
async def read_user(user_id: int, db: Session = db_dependency):
    return db_user.get_user_by_id(user_id, db)

@router.put('/update/current_user', status_code=status.HTTP_200_OK, response_model=UserDisplay)
async def update_user(user: UserBase,  db: Session = db_dependency, current_user: User = Depends(get_current_user)):
    return db_user.update_current_user(user, db, current_user)

@router.delete('/delete/by_id/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = db_dependency):
    return db_user.delete_by_id(user_id, db)