from typing import List,Optional
from pydantic import BaseModel

from auth.Oauth2 import get_curr_user


class BlogBase(BaseModel):
    title : str
    content : str
    published : Optional[bool] = False
    creator_id: Optional[int]

class BlogDisplay(BaseModel):
    title: str
    content: str
    published : Optional[bool]
    class Config():
        orm_mode = True



