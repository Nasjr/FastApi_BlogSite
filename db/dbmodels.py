from sqlalchemy import Column, DateTime, Integer,String,Enum
from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from schemas.users_schemas import Role


class DbBlog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, default = False)
    creationDate = Column(DateTime(timezone=True),server_default=func.now())
    updateDate = Column(DateTime(timezone=True),onupdate=func.now())
    creator_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
    image_url = Column(String)
    user = relationship('DbUser', back_populates='items',passive_deletes=True)




class DbUser(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String)
  email = Column(String)
  password = Column(String)
  role = Column(Enum(Role), default="User")
  items = relationship('DbBlog', back_populates='user',passive_deletes=True)

