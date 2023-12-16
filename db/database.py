from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



SQLALCHEMY_DB_URL = 'sqlite:///./blog.db'

engine = create_engine(SQLALCHEMY_DB_URL,connect_args={'check_same_thread':False})

Sessionlocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)


Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
