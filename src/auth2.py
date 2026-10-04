import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import config, schemas, models
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import HTTPException, status,Depends
from sqlalchemy.orm import Session
from .database import get_db

    
SECRET_KEY =config.settings.secret_key
ALGORITHM =config.settings.algorithm
def create_access_token(data : dict):

    to_encode = data.copy()
    expiretime = datetime.now(timezone.utc) + timedelta(minutes=config.settings.access_token_expire_minutes)
    to_encode.update({ 'exp' : expiretime})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return  { 'access_token' : encoded_jwt, "token_type" : "bearer"} 

def verify_access_token(token :str , credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        
        id: int = payload.get("userid")
        
        if id is None:
            raise credentials_exception

        token_data = schemas.Tokendata(id = id)
        
    except InvalidTokenError:
        raise credentials_exception

    return token_data

oauth2_scheme  = OAuth2PasswordBearer(tokenUrl= 'login')
def get_current_user(token : str = Depends(oauth2_scheme),db:Session =  Depends(get_db) ):
    credentials_exception =HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail=f"Please Login to continue !!", headers={'WWW-Authenticate': "Bearer"})
    token = verify_access_token(token, credentials_exception)
   
    user_detail = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user_detail
    