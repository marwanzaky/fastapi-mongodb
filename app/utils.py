from passlib.context import CryptContext;
from fastapi import HTTPException, status
from datetime import timedelta, datetime
from jose import JWTError, jwt

import os
import app.schemas as schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password, hashed_pass):
    return pwd_context.verify(password, hashed_pass)

def create_access_token(data: dict) -> str:
    token_expire_minutes = int(os.environ.get("TOKEN_EXPIRE_MINUTES"))
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=token_expire_minutes)
    to_encode.update({
        "expire": expire.strftime("%Y-%m-%d %H:%M:%S")
    })

    encoded_jwt = jwt.encode(to_encode, os.environ.get("TOKEN_SECRET_KEY"), algorithm=os.environ.get("TOKEN_ALGORITHM"))

    return encoded_jwt

def verify_token_access(token: str, credentials_exception: HTTPException) -> schemas.DataToken:
    try:
        payload: dict = jwt.decode(token, os.environ.get("TOKEN_SECRET_KEY"), algorithms=os.environ.get("TOKEN_ALGORITHM"))

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.DataToken(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    return token_data

def get_current_user(token: str, users_collection) -> dict:
    credentials_exception = HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Could not validate credentials",
            headers= {"WWW-Authenticate": "Bearer"}
        )

    token: schemas.DataToken = verify_token_access(token, credentials_exception)

    user = users_collection.find_one(
        {"_id": token.id}
    )

    return user