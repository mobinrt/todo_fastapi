from DB.models import User
from fastapi import HTTPException, status
from sqlalchemy.orm import Session 

import hash
from schemas import UserDisplay, UserBase

def create_user(new_user: User, db: Session):
    user = db.query(User).filter(User.username == new_user.username).first()  
        
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    
    hash_password = hash.get_password_hash(new_user.password)
    db_user = User(username=new_user.username, hashed_password=(hash_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()    
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

def get_user_by_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()    
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

def get_all_users(db: Session):
    users = [] 
    users = db.query(User).all()
    return [UserDisplay(**user.__dict__) for user in users]

def update_current_user(user: UserBase, db: Session, current_user: User):
    for var, value in vars(user).items():
        setattr(current_user, var, value) if value else None

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

def delete_by_id(user_id: int, db: Session):
    del_user = get_user_by_id(user_id, db)

    if not del_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        
    db.delete(del_user)
    db.commit()
    return {"detail": "User deleted successfully"}