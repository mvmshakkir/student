from typing import List
from fastapi import APIRouter,Depends,HTTPException, status,Request
from ..import schemas,database,models,oauth2
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..repository import students
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

router=APIRouter(
     prefix="/students",
    tags=['Students']
)
templates=Jinja2Templates(directory="templates")

@router.get('/',response_model=list[schemas.ShowStudent])
def Get_user(db:Session=Depends(database.get_db),current_user:schemas.Student=Depends(oauth2.get_current_user)):
   return students.getall(db)

# @router.get('/{id}',response_model=schemas.ShowStudent)
# def single_user(id:int,db:Session=Depends(database.get_db)):
#     user = students.getstd(id, db)
#     return templates.TemplateResponse("edituser.html", {"request": Request, "user": user})
    # return students.getstd(id,db)


@router.get("/hello/", response_class=HTMLResponse)
async def hello(request: Request):
   return templates.TemplateResponse("register.html", {"request": request})

@router.post('/register')
def create(request:schemas.Student,db:Session=Depends(database.get_db)):
    return students.Create(request,db)

# @router.put("/update/{id}")
# def update(int:id,request:schemas.ShowStudent,db: Session=Depends(database.get_db)):
#    st=db.query(models.Student).filter(models.Student.id==id).first()
