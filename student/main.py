from typing import List
from fastapi import FastAPI,Depends,HTTPException, status

from .import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app=FastAPI()

models.Base.metadata.create_all(engine)
def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()  
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
@app.post('/student')
def create(request:schemas.Student,db:Session=Depends(get_db)):
    if request.password != request.conform_password:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and confirm password do not match"
        )
       
    else:
        hashedPassword=pwd_context.hash(request.password)
        new_user = models.Student(
            name=request.name,
            department=request.department,
            father_name=request.father_name,
            place=request.place,
            mobile=request.mobile,
            email=request.email,
            password=hashedPassword,
            conform_password=hashedPassword
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    

@app.get('/getuser',response_model=list[schemas.ShowStudent])
def Get_user(db:Session=Depends(get_db)):
    Users=db.query(models.Student).all()
    return Users

@app.get('/getuser/{id}',response_model=schemas.ShowStudent)
def single_user(id,db:Session=Depends(get_db)):
    users =db.query(models.Student).filter(models.Student.id==id).first()
    return users