from typing import List,Optional
from pydantic import BaseModel


class Student(BaseModel):
    name:str
    department :str
    father_name: str
    place :str
    mobile:str
    email:str
    password:str
    conform_password:str
    
class ShowStudent(BaseModel):
    name:str
    department :str
    father_name: str
    place :str
    mobile:str
    email:str

    class Config():
        orm_mode=True  
class ps(BaseModel):
    password:str
    conform_password:str
    class Config():
        orm_mode=True  
class Login(BaseModel):
    username:str
    password:str



class StudentBase(BaseModel):
    password:str
    conform_password:str

class Blog(StudentBase):
    class Config():
        orm_mode=True    


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str]=None  
