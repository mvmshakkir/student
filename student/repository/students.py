from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import APIRouter,Depends,HTTPException, status,Form
from passlib.context import CryptContext
from ..hashing import Hash
from fastapi.templating import Jinja2Templates
import logging

def getall(db:Session):
    Users=db.query(models.Student).all()
    return Users

templates=Jinja2Templates(directory="templates")

def getstd(id:int,db:Session):
    users =db.query(models.Student).filter(models.Student.id==id).first()
    return users

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def Create(request:schemas.Student,db:Session
          ):
   
   if request.password != request.conform_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and confirm password do not match"
        )
   else:
        
        
        new_user = models.Student(
            name=request.name,
            department=request.department,
            father_name=request.father_name,
            place=request.place,
            mobile=request.mobile,
            email=request.email,
            password=Hash.bcrypt(request.password),
            conform_password=Hash.bcrypt(request.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
   
   
