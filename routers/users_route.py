from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from auth.Oauth2 import get_curr_user
# from auth.oauth2 import get_curr_user
from db.database import get_db
from db import users_db
from schemas.users_schemas import Role, UserBase, UserDisplay
from sqlalchemy.orm import Session

router = APIRouter(prefix='/user',tags=['user'])

#Create user

@router.post('/',response_model=UserDisplay)
def create_user(request:UserBase , db : Session = Depends(get_db)):
    return users_db.create_user(request,db)

# Read all users
@router.get('/all',response_model = List[UserDisplay])
def get_all_users(db : Session = Depends(get_db),curr_user: UserBase = Depends(get_curr_user)):
        if curr_user.role == Role.Admin:
            users =  users_db.get_all_users(db)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Admins only can get all users')
        return users

# read user
@router.get('/{id}',response_model = UserDisplay)
def get_user(id: int ,db : Session = Depends(get_db),curr_user: UserDisplay = Depends(get_curr_user)):
    if curr_user.role == Role.Admin or curr_user.id == id:
        user = users_db.get_user_by_id(id=id,db=db)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Admins only can get users by id')
    return user

# Update user
@router.post('/{id}/update')
def update_user(id : int , requset: UserBase, db:Session = Depends(get_db),curr_user: UserBase = Depends(get_curr_user)):
    if curr_user.role == Role.Admin or curr_user.id == id:
        users_db.update_user(id,requset,db)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Admins or owenrs only can update users by id')
    return {'Message':{f'User with id {id} update successfully'}}


# Delete user
@router.delete('/{id}/delete')
def delete_user(id : int , db:Session = Depends(get_db),curr_user: UserBase = Depends(get_curr_user)):
    if curr_user.role == Role.Admin or curr_user.id == id:
        users_db.delete_user(id,db)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Admins or account owners only can get delete by id')
    return {'Message':{f'User with id {id} deleted successfully'}}
