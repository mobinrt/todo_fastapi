from fastapi import Body
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    password: str = Body(min_length=6, max_length=16)
    
class UserDisplay(BaseModel):
    username: str
    todo_num : int 

    class Config:
        from_attributes = True
    
class TodoBase(BaseModel):  
    task: str
    description: Optional[str] = None
    completed: bool = False
    created_id: int

class TodoCreate(BaseModel):
    task: str
    description: Optional[str] = None
    completed: bool = False

class TodoDisplay(BaseModel):
    task: str
    description: Optional[str] = None
    completed: bool = False
    
    class Config:
        from_attributes = True    

class TodoUpdate(BaseModel):
    description: Optional[str] = None
    completed: bool = False

class TokenDisplay(BaseModel):
    access_token: str
    token_type: str
    
    class Config:
        from_attributes = True
        