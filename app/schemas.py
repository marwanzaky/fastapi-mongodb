from typing import Literal, Optional, Any
from pydantic import BaseModel, EmailStr

class ResponseModel(BaseModel):
    status: Literal['success', 'failed']
    message: str
    data: Any
    
class LoginUser(BaseModel):
    email: str
    password: str

class CreateUser(BaseModel):
    fname: Optional[str]
    email: EmailStr
    password: str
    # created_at: datetime.datetime

class UpdateUser(BaseModel):
    fname: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DataToken(BaseModel):
    id: Optional[str] = None
