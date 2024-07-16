from fastapi import Security, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import secrets

from DB.database import get_db
from DB.db_user import get_user_by_username

oauth2_sc = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None): 
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str=Security(oauth2_sc), db: Session= Depends(get_db)):
    custom_error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail='Invalid credentials')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise custom_error
    except JWTError:
        raise custom_error
                                 
    user = get_user_by_username(username, db)
    if user is None:
        raise custom_error
    return user