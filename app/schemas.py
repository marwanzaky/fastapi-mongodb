from typing import Literal, Optional, Any
from pydantic import BaseModel, EmailStr, constr

from datetime import datetime

class ResponseModel(BaseModel):
    status: Literal['success', 'failed']
    message: str
    data: Any
    
class LoginUser(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class CreateUser(BaseModel):
    role: Literal['user', 'admin'] = None
    name: Optional[str]
    email: EmailStr
    password: constr(min_length=8)
    password_confirm: str
    created_at: datetime = None
    verified: bool = None

class UpdateUser(BaseModel):
    name: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class DataToken(BaseModel):
    id: Optional[str] = None
