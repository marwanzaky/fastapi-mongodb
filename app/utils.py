from passlib.context import CryptContext;
from fastapi import HTTPException, Request, status
from datetime import timedelta, datetime
from jose import JWTError, jwt
from pymongo.collection import Collection
from bson.objectid import ObjectId

import os
import app.schemas as schemas

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return pwd_context.verify(password, hashed_pass)

def create_access_token(data: dict) -> str:
    token_expire_minutes: str = os.environ.get("TOKEN_EXPIRE_MINUTES")
    token_secret_key: str = os.environ.get("TOKEN_SECRET_KEY")
    token_algorithm: str = os.environ.get("TOKEN_ALGORITHM")

    token_expire_minutes_int: int = int(token_expire_minutes)
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=token_expire_minutes_int)
    to_encode.update({
        "expire": expire.strftime("%Y-%m-%d %H:%M:%S")
    })

    encoded_jwt = jwt.encode(to_encode, token_secret_key, algorithm=token_algorithm)

    return encoded_jwt

def verify_token_access(token: str, credentials_exception: HTTPException) -> schemas.DataToken:
    token_secret_key: str = os.environ.get("TOKEN_SECRET_KEY")
    token_algorithm: str = os.environ.get("TOKEN_ALGORITHM")

    try:
        payload: dict = jwt.decode(token, token_secret_key, algorithms=token_algorithm)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.DataToken(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    return token_data

def get_current_user(token: str, users_collection: Collection) -> dict:
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

async def protect(request: Request):
    token: str = None

    users_collection: Collection = request.app.users_collection

    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate credentials",
        headers= {"WWW-Authenticate": "Bearer"}
    )

    if request.headers.get('authorization') and request.headers.get('authorization').startswith('Bearer'):
        token: str = request.headers.get('authorization').split(' ')[1]

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in. Please log in to get access")

    dataToken: schemas.DataToken = verify_token_access(token, credentials_exception)

    user = users_collection.find_one(
        {"_id": ObjectId(dataToken.id)},
        {"_id": 0, "password": 0}
    )

    user["id"] = dataToken.id

    request.app.user = user