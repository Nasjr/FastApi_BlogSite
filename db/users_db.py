from db.dbmodels import DbUser
from sqlalchemy.orm import Session

from schemas.users_schemas import UserBase, UserDisplay
from auth import hash
def get_all_users(db:Session):
    return db.query(DbUser).all()


def get_user_by_id(id:int , db:Session):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    return user


def get_user_by_username(user_name:str,db:Session):
    user = db.query(DbUser).filter(DbUser.username == user_name).first()
    return user

def create_user(request:UserBase,db:Session):
    new_user = DbUser(username=request.username,password=hash.get_hashed_password(request.password),email=request.email,role=request.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

def update_user(id:int,request:UserBase,db:Session):
    user = db.query(DbUser).filter(DbUser.id == id)
    new_user = user.update({
        DbUser.email : request.email,
        DbUser.username : request.username,
        DbUser.password : hash.get_hashed_password(request.password)
    })
    db.commit()
    return {'message':f'updated user With id {id}'}

def delete_user_by_id(id:int,db:Session):
    user = db.query(DbUser).filter(DbUser.id == id)
    user.delete()
    db.commit()
    return {'message':f'deleted user With id {id}'}
