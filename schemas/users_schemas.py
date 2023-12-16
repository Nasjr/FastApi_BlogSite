from enum import Enum
from typing import List,Optional
from fastapi import HTTPException
from pydantic import BaseModel



# this will be in the api function
class Role(str,Enum):
    Admin = 'Admin'
    user = "User"


class UserBase(BaseModel):
    username:str
    email:str
    password:str
    role: Optional[Role] = Role.Admin



class UserBlog(BaseModel):
    title:str
    content:str
    published:bool
    class Config():
        orm_mode = True


class UserDisplay(BaseModel):
    id:int
    username:str
    email:str
    userBlogs : List[UserBlog] = []
    class Config():
        orm_mode = True
    