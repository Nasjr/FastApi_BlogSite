from datetime import timedelta,datetime
from typing import Optional
from fastapi import Depends, HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm.session import Session
from db import users_db

from db.database import get_db

oauth2_shceme = OAuth2PasswordBearer(tokenUrl='token')


SECRET_KEY = '4c4b9da275fe979dabbb7862a21a3c1518f13b38cf3ccec621f84d838e7da817'
ALGORITHM = 'HS256'

ACCESS_TOKEN_EXPIRY_MINUTES = 30


def create_access_token(data:dict,expiry_delta:Optional[timedelta] = None):
    to_encode = data.copy()
    if expiry_delta:
        expire = datetime.utcnow() + expiry_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt


def get_curr_user(token:str = Depends(oauth2_shceme), db :Session = Depends(get_db)):
    credentials_execption = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail= 'Faild to validate credentials',headers={'WWW-Authenticate':"Bearer"})
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_execption
    except JWTError:
        raise credentials_execption
    user = users_db.get_user_by_username(username,db)
    if user is None:
        raise credentials_execption
    return user



