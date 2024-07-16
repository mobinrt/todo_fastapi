from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.orm import Session
from datetime import timedelta
from AUTH import auth_usecase
from schemas import TokenDisplay

from DB.database import get_db

router = APIRouter(tags=['athentication'])
    
@router.post('/token', response_model=TokenDisplay, status_code=status.HTTP_200_OK)      #chera token bayad bashe??
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    return auth_usecase.get_token(request, db)