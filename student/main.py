from typing import List
from fastapi import FastAPI,Depends,HTTPException, status,Request

from .import schemas,models,database,oauth2,token,hashing
# from .oauth2 import get_current_user
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from .routers import students,authentication,password_reset
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
# from .repository import students
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from .hashing import Hash

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME="mshakkirmv@gmail.com",
    MAIL_PASSWORD="brayrvprgliyxtuq",
    MAIL_FROM="mshakkirmv@gmail.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,  # Disable STARTTLS
    MAIL_SSL_TLS=True,    # Enable SSL/TLS
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)



app=FastAPI(
)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(engine)
app.include_router(students.router)
app.include_router(password_reset.router)
app.include_router(authentication.router)
template_file_path = "update_pw.html"

@app.post("/email")
async def simple_send(email:str,db: Session=Depends(database.get_db)) -> JSONResponse:
    reset_url = "http://127.0.0.1:8000/update_pw"
   
    student=db.query(models.Student).filter(models.Student.email==email).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credential")
    access_token = token.create_access_token(data={"sub": student.email})
    reset_token = models.PasswordResetTokenn(email=email, token=access_token)
    email_content = f"""
    <html>
        <body>
            <p>To reset your password, click 
            <a href="{reset_url}?token={access_token}&email={email}">here</a>.</p>
            
            <form action="{reset_url}" method="post">
                <input type="hidden" name="token" value="{access_token}">
                <input type="hidden" name="email" value="{email}">
            </form>
        </body>
    </html>
"""

    db.add(reset_token)
    db.commit()
    db.refresh(reset_token)
    message = MessageSchema(
        subject="Reset Password",
        recipients=[email],
        body=email_content,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

@app.get("/register", response_class=HTMLResponse)
async def hello(request: Request):
   return templates.TemplateResponse("register.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
   return templates.TemplateResponse("login.html", {"request": request})

@app.get('/home',response_class=HTMLResponse)
async def home(request: Request,  db: Session = Depends(database.get_db)):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/edit/{id}", response_class=HTMLResponse,response_model=schemas.ShowStudent)
async def hello(request: Request,id:int,db:Session=Depends(database.get_db) ):
        user=db.query(models.Student).filter(models.Student.id==id).first()
        return templates.TemplateResponse("edituser.html", {"request": request,"user":user})

@app.post("/update/{id}")
async def update_student(id: int, updated_student: schemas.ShowStudent, db: Session = Depends(database.get_db)):
    existing_student = db.query(models.Student).filter(models.Student.id == id).first()
    
    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update the student's attributes with the new data
    if updated_student.name:
        existing_student.name = updated_student.name

    if updated_student.father_name:
        existing_student.father_name = updated_student.father_name
    if updated_student.place:
        existing_student.place = updated_student.place    
    if updated_student.mobile:
        existing_student.mobile = updated_student.mobile
    if updated_student.department:
        existing_student.department = updated_student.department   
    db.commit()
    db.refresh(existing_student)
    
    return {"message": "Student updated successfully", "updated_student": existing_student}

@app.get("/reset", response_class=HTMLResponse)
async def reset(request: Request):
   return templates.TemplateResponse("reset_password.html", {"request": request})
@app.get("/success_pw")
async def reset(request: Request):
   return templates.TemplateResponse("success_pw.html", {"request": request})
@app.get("/update_pw")
async def reset(request: Request):
   return templates.TemplateResponse("update_pw.html", {"request": request})
@app.post('/updtps', status_code=status.HTTP_202_ACCEPTED )
def update(token:str,email:str,request:schemas.ps,db: Session=Depends(database.get_db)):
    up=db.query(models.PasswordResetTokenn).filter(models.PasswordResetTokenn.token==token).first()
    st=db.query(models.Student).filter(models.Student.email==email).first()
    if not up:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with the token is not available")
    email = up.email
    student = db.query(models.Student).filter(models.Student.email ==email).first()
    if not up:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the email is not available")
    if request.password != request.conform_password:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and confirm password do not match"
        ) 
    hashed_password = Hash.bcrypt(request.password)
    
    # Ensure student is not None before updating the password
    if student:
        student.password = hashed_password
        student.conform_password = hashed_password
        db.commit()
        return {"message": "Password updated successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    