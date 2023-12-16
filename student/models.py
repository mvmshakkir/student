from sqlalchemy import Column,Integer,String
from .database import Base


class Student(Base):
    __tablename__='student'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    department=Column(String)
    father_name=Column(String)
    place =Column(String)
    mobile=Column(String)
    email=Column(String)
    password=Column(String)
    conform_password=Column(String)