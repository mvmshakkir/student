from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..import schemas,database,models,token,oauth2
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi.responses import HTMLResponse,RedirectResponse

from fastapi.templating import Jinja2Templates
router=APIRouter(
    
    tags=['Authentication']
)
templates=Jinja2Templates(directory="templates")

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db: Session=Depends(database.get_db)):
 

    student=db.query(models.Student).filter(models.Student.email==request.username).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credential")
    if not Hash.verify(student.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect Password")
   
    access_token = token.create_access_token(data={"sub": student.email})
    
    return {"access_token": access_token, "token_type": "bearer","student_id":student.id}
    # redirect_url = f"/home?access_token={access_token}&token_type=bearer"
    # return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
def get_user(email:str,db: Session):
    user = db.query(models.Student).filter(models.Student.email == email).first()
    return user