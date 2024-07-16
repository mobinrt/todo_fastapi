from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List

from schemas import TodoBase, TodoDisplay, TodoUpdate, TodoCreate
from DB.database import get_db
from DB import db_todo
from DB.models import User
from AUTH.oauth2 import get_current_user

db_dependency = Depends(get_db)

router = APIRouter(prefix='/todo', tags=['todo'])

@router.post('/create/', response_model=TodoDisplay, status_code=status.HTTP_201_CREATED)   #C
async def create_todo(todo: TodoCreate, db: Session = db_dependency, current_user: User=Depends(get_current_user)):
    return db_todo.create_todo(todo, db, current_user)

@router.get('/get/all/', response_model=List[TodoDisplay], status_code=status.HTTP_200_OK)     #R
async def read_todos(db: Session = db_dependency, current_user: User = Depends(get_current_user)):
    return db_todo.get_all_todos(db, current_user.id)
    
@router.get('/get/by/id/{todo_id}', response_model=TodoDisplay, status_code=status.HTTP_200_OK)    #R
async def read_todo(todo_id: int, db: Session = db_dependency, current_user: User = Depends(get_current_user)):
    return db_todo.get_todo_by_id(todo_id, db, current_user.id)
    
@router.put('/update/by/id/{todo_id}', response_model=TodoDisplay, status_code=status.HTTP_200_OK)    #U
async def update_todo(todo_id: int, todo: TodoUpdate, db: Session = db_dependency, current_user: User = Depends(get_current_user)):
    return db_todo.update_todo(todo_id, todo, db, current_user.id)

@router.delete('/delete/by_id/{todo_id}',  status_code=status.HTTP_204_NO_CONTENT)    #D
async def delete_todo(todo_id: int, db: Session = db_dependency, current_user: User = Depends(get_current_user)): 
    return db_todo.delete_todo_by_id(todo_id, db, current_user)
    
   
   
    
'''
@router.put('/complete/by/id/{todo_id}', status_code=status.HTTP_200_OK)    #U
async def complete_todo(todo_id: int, db: Session = db_dependency, current_user: User = Depends(get_current_user)):
'''