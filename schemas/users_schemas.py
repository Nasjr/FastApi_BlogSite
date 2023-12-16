from enum import Enum
from typing import List,Optional
from fastapi import HTTPException
from pydantic import BaseModel



# this will be in the api function
class Role(Enum):
    Admin = 'Admin'
    User = "User"


class UserBase(BaseModel):
    username:str
    email:str
    password:str
    role: Optional[Role] = Role.User



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
    role: Role
    userBlogs : List[UserBlog] = []
    class Config():
        orm_mode = True
    