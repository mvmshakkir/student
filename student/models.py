from sqlalchemy import Column,Integer,String,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    token = Column(String)  
    # creator=relationship("Student",back_populates="std")
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
    # std=relationship('PasswordResetToken',back_populates="creator")

