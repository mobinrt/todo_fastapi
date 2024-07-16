from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from schemas import TodoBase, TodoCreate, TodoUpdate
from DB.models import Todo, User


def create_todo(todo: TodoCreate, db: Session, current_user: User):
    #if todo.task is None:
        
    db_todo = Todo(user_id=current_user.id, **todo.model_dump())
    db.add(db_todo)
    current_user.todo_num += 1
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_all_todos(db: Session, user_id: int):
    todos = []
    todos = db.query(Todo).filter(Todo.user_id == user_id).all()
    if not todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No items found in the list")
    return todos

def get_todo_by_id(todo_id: int, db: Session, user_id: int):
    todo = db.query(Todo).filter(Todo.user_id == user_id, Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    return todo

def update_todo(todo_id: int, todo: TodoUpdate, db: Session, user_id: int):
    db_todo = get_todo_by_id(todo_id, db, user_id)
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    for key, value in todo.model_dump().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo_by_id(todo_id: int, db: Session, current_user: User):
    db_todo = get_todo_by_id(todo_id, db, current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    
    current_user.todo_num -= 1
    db.delete(db_todo)
    db.commit()
    return {"detail": "Your task deleted successfully"}