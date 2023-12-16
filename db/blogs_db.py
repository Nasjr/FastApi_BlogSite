from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException,status
from db.database import get_db

from db.dbmodels import DbBlog
from schemas.blog_schemas import BlogBase
from schemas.users_schemas import UserBase
def get_all_blogs(db = Session):
    blogs = db.query(DbBlog).all()
    return blogs

def get_blog_by_id(id :int, db : Session):
    blogs = db.query(DbBlog).filter(DbBlog.id == id).first()
    return blogs


def create_blog(request: BlogBase , db : Session , curr_user_id:int):
    try:
        new_blog = DbBlog(title = request.title, content = request.content,creator_id = curr_user_id)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
    except: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="Database error while trying to create user")
    return new_blog

def delete_blog(id : int,db : Session):
    try:
        new_blog = db.delete.filter(DbBlog.id == id).first()
    except: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} as not found")
    return new_blog

def update_blog(id:int , request: BlogBase, db:Session, creator_id:int):
    # handel exceptions
    blog = db.query(DbBlog).filter(DbBlog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} as not found")
    blog.update({
        DbBlog.title : request.title,
        DbBlog.content : request.content,
        DbBlog.published : request.published,
        DbBlog.creator_id: creator_id
    })
    db.commit()
    return 'ok'


