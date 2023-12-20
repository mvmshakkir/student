from typing import List
from fastapi import APIRouter,Depends,HTTPException, status
from ..import schemas,database,models,oauth2
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..repository import students
router=APIRouter(
     prefix="/students",
    tags=['Students']
)


@router.get('/',response_model=list[schemas.ShowStudent])
def Get_user(db:Session=Depends(database.get_db),current_user:schemas.Student=Depends(oauth2.get_current_user)):
   return students.getall(db)

@router.get('/{id}',response_model=schemas.ShowStudent)
def single_user(id:int,db:Session=Depends(database.get_db),current_user:schemas.Student=Depends(oauth2.get_current_user)):
    return students.getstd(id,db)



@router.post('/')
def create(request:schemas.Student,db:Session=Depends(database.get_db)):
    return students.Create(request,db)