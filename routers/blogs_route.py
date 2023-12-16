from fastapi import APIRouter, HTTPException, Query , Body , Path
from typing import List, Union
from fastapi import Depends,status,Response

from auth.Oauth2 import get_curr_user
from db.database import get_db
from schemas.blog_schemas import BlogDisplay,BlogBase
from db import blogs_db
from sqlalchemy.orm import Session

from schemas.users_schemas import Role, UserBase, UserDisplay


router = APIRouter(prefix = '/blog',tags = ['blogs'])

@router.get('/all',status_code=status.HTTP_200_OK)
def get_all_blogs( response : Response,db : Session = Depends(get_db), curr_user: UserDisplay = Depends(get_curr_user)):
    blogs = blogs_db.get_all_blogs(db)
    if len(blogs) == 0 :
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="The database dosen't contain any data")
    return blogs_db.get_all_blogs(db)

@router.get('/{id}')
def get_blog_by_id(id:int,db : Session = Depends(get_db), curr_user: UserDisplay = Depends(get_curr_user)):
        blog = blogs_db.get_blog_by_id(id,db)
        if not blog:
             return HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} as not found")    
        return blog

# @router.post('/create', response_model = BlogDisplay)
# def get_blog_by_id(request:BlogBase, db : Session = Depends(get_db), curr_user:UserBase = Depends(get_curr_user)):
#     return blogs_db.create_blog(request,db)    

@router.post('/new/blog')
def create_blogs(blog_request : BlogBase, db : Session = Depends(get_db), current_user: UserBase = Depends(get_curr_user)):
    new_blog = blogs_db.create_blog(blog_request,db,curr_user_id=current_user.id)   
    return {
        'data':new_blog,
        'current_user':current_user
        }


@router.put('/{id}')
def update_blog_by_id(id:int,updated_blog : BlogDisplay,db : Session = Depends(get_db), curr_user: UserDisplay = Depends(get_curr_user)):
        curr_blog = blogs_db.get_blog_by_id(id,db)
        if not curr_blog:
             raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} as not found")
        if curr_user.id != curr_blog.creator_id:
             
              raise HTTPException(status_code = 402,detail=f"Not Authoraized only creator of the post can modify it")   
         
        return blogs_db.update_blog(id,updated_blog,db,curr_user.id)

@router.delete('/{id}')
def delete_blog_by_id(id:int,db : Session = Depends(get_db), curr_user: UserDisplay = Depends(get_curr_user)):
        blog = blogs_db.get_blog_by_id(id,db)
        if not blog:
             print('Not Found'*20)
             raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} as not found") 
        if int(curr_user.id) != int(blog.creator_id) or curr_user.role.value != Role.User:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} Can only be modified by owner or Admins")
        return blogs_db.delete_blog(id,db)