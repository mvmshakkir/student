from typing import List
from fastapi import FastAPI,Depends,HTTPException, status

from .import schemas,models
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session

from .routers import students,authentication,password_reset

app=FastAPI(
)

models.Base.metadata.create_all(engine)
app.include_router(students.router)
app.include_router(password_reset.router)
app.include_router(authentication.router)
