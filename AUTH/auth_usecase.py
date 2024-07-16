from fastapi import HTTPException, status

from DB import models
from AUTH import oauth2
import hash
from schemas import TokenDisplay


def get_token(request, db):
    custome_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password ",
                            headers={"WWW-Authenticate": "bearer"}
                            )
        
    user = db.query(models.User).filter(models.User.username == request.username).first()
    
    if not user or not hash.verify_password(request.password, user.hashed_password):
        raise custome_error
                  
    access_token = oauth2.create_access_token(data = {'sub' : user.username})
    print(user.username)
    return TokenDisplay(access_token=access_token, token_type='bearer')

            