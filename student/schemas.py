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