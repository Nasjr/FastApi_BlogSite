from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from db.database import get_db
from db.dbmodels import DbUser
from auth.hash import verify_hashed_password
from auth import Oauth2

router = APIRouter(tags=['authentication'])


@router.post('/token')
def get_token(request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):

    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    print(request.username,request.password)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = 'Invalid Credentials')
    if not verify_hashed_password(request.password,user.password):
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = 'Invalid Credentials')
    access_token = Oauth2.create_access_token(data={'sub':user.username},expiry_delta=timedelta(minutes=30))
    return {'access_token':access_token,'token_type':'bearer'}


