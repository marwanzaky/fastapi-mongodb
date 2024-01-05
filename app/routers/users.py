from fastapi import APIRouter, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from bson.objectid import ObjectId
from app.utils import verify_token_access, create_access_token, verify_password, hash_pass

import app.schemas as schemas

router = APIRouter()

@router.get("/me", status_code=status.HTTP_200_OK, response_model=schemas.ResponseModel)
async def me(request: Request) -> schemas.ResponseModel:
    users_collection: Collection = request.app.users_collection

    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate credentials",
        headers= {"WWW-Authenticate": "Bearer"}
    )

    token: str = request.headers.get('authorization').split(' ')[1]

    dataToken: schemas.DataToken = verify_token_access(token, credentials_exception)

    user = users_collection.find_one(
        {"_id": ObjectId(dataToken.id)},
        {"_id": 0, "password": 0}
    )

    return schemas.ResponseModel(status='success', message="User successfully loaded", data={"user": user})

@router.patch("/me", status_code=status.HTTP_200_OK, response_model=schemas.ResponseModel)
async def me(request: Request, updateUser: schemas.UpdateUser) -> schemas.ResponseModel:
    users_collection: Collection = request.app.users_collection

    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate credentials",
        headers= {"WWW-Authenticate": "Bearer"}
    )

    token: str = request.headers.get('authorization').split(' ')[1]

    dataToken: schemas.DataToken = verify_token_access(token, credentials_exception)

    users_collection.update_one(
        {"_id": ObjectId(dataToken.id)},
        { "$set": { "fname": updateUser.fname, "email": updateUser.email } }
    )
    
    updated_user = users_collection.find_one(
        {"_id": ObjectId(dataToken.id)},
        {"_id": 0, "password": 0}
    )

    return schemas.ResponseModel(status="success", message="User successfully updated", data={"user": updated_user})

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(request: Request):
    users_collection: Collection = request.app.users_collection

    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate credentials",
        headers= {"WWW-Authenticate": "Bearer"}
    )

    token: str = request.headers.get('authorization').split(' ')[1]

    dataToken: schemas.DataToken = verify_token_access(token, credentials_exception)

    users_collection.delete_one({"_id": ObjectId(dataToken.id)})

    return None

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.ResponseModel)
async def login(request: Request, loginUser: schemas.LoginUser) -> schemas.ResponseModel:
    users_collection: Collection = request.app.users_collection

    user = users_collection.find_one(
        {"email": loginUser.email}
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist")
    
    if not verify_password(loginUser.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password do not match")
    
    access_token = create_access_token(data={"user_id": str(user["_id"])})

    return schemas.ResponseModel(status="success", message="User successfully logged", data={"access_token": access_token, "token_type": "bearer"})

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseModel)
async def create_user(request: Request, user: schemas.CreateUser) -> schemas.ResponseModel:
    try:
        users_collection: Collection = request.app.users_collection

        hashed_pass = hash_pass(user.password)

        user.password = hashed_pass
        user = jsonable_encoder(user)

        new_user = users_collection.insert_one(user)
        created_user = users_collection.find_one(
            {"_id": new_user.inserted_id},
            {"_id": 0, "password": 0}
        )

        return schemas.ResponseModel(status="success", message="User successfully created", data={"user": created_user})
    except DuplicateKeyError:
        return schemas.ResponseModel(status="failed", message="User with the same email already exists", data=None)
