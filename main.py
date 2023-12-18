# E:\Courses\Python\BlogApi\blogapivenv\Scripts\activate.bat 
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import dbmodels
from db.database import engine, Sessionlocal
from sqlalchemy.orm import Session
from routers import blogs_route,users_route
from auth import authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(blogs_route.router)

app.include_router(users_route.router)
app.mount('/images',StaticFiles(directory='images'),name='images')

dbmodels.Base.metadata.create_all(bind = engine)

@app.get('/')
def index():
    return {'messsage':"This is the main route"}


