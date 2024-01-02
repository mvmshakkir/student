from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .import schemas,models,database,oauth2
from sqlalchemy.orm import Session


SQLALCHEMY_DATABASE_URL='sqlite:///./student.db'
engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})

# SQLALCHEMY_DATABASE_URL='sqlite:///./student.db'

# engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args=
#                      {"check_same_thread":False})

SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()  


def get_user_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email==email).first()