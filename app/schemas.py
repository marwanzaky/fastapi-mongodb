from typing import Optional
from pydantic import BaseModel, EmailStr

import datetime

class User(BaseModel):
    id: str
    fname: Optional[str]
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

class CreateUser(BaseModel):
    fname: Optional[str]
    email: str
    password: str

class OutputUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class DataToken(BaseModel):
    id: Optional[str] = None

class UpdateUser(BaseModel):
    fname: str
    email: str