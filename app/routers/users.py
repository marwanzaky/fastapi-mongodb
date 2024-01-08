from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from bson.objectid import ObjectId

from datetime import datetime

from typing import Annotated
from fastapi import UploadFile, Form, File

import app.utils as utils
import app.schemas as schemas
import bson.binary

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.ResponseModel)
async def login(request: Request, loginUser: schemas.LoginUser) -> schemas.ResponseModel:
    users_collection: Collection = request.app.users_collection

    user = users_collection.find_one(
        {"email": loginUser.email}
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist")
    
    if not utils.verify_password(loginUser.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password do not match")
    
    access_token = utils.create_access_token(data={"user_id": str(user["_id"])})

    return schemas.ResponseModel(status="success", message="User successfully logged", data={"access_token": access_token, "token_type": "bearer"})

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseModel)
async def create_user(request: Request, user: schemas.CreateUser) -> schemas.ResponseModel:
    try:
        users_collection: Collection = request.app.users_collection

        if user.password != user.password_confirm:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')

        del user.password_confirm
        hashed_pass = utils.hash_pass(user.password)
        user.password = hashed_pass

        user.role = 'user'
        user.created_at = datetime.utcnow()
        user.verified = False

        user = jsonable_encoder(user)

        new_user = users_collection.insert_one(user)
        created_user = users_collection.find_one(
            {"_id": new_user.inserted_id},
            {"_id": 0, "password": 0}
        )

        return schemas.ResponseModel(status="success", message="User successfully created", data={"user": created_user})
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with the same email already exists')

# protected
router.dependencies=[Depends(utils.protect)]

# /me
@router.get("/me", status_code=status.HTTP_200_OK, response_model=schemas.ResponseModel)
async def me(request: Request) -> schemas.ResponseModel:
    return schemas.ResponseModel(status='success', message="User successfully loaded", data={"user": request.app.user})

@router.patch("/me", status_code=status.HTTP_200_OK)
async def update_me(request: Request, name: Annotated[str, Form()], email: Annotated[str, Form()], picture: Annotated[UploadFile, File()]):
    picture_contents = await picture.read()

    user: dict = request.app.user
    users_collection: Collection = request.app.users_collection

    user_update = {
        "name": name,
        "email": email
    }

    if picture_contents:
        user_update["picture"] = bson.binary.Binary(picture_contents)

    users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        { "$set": user_update }
    )
    
    updated_user: dict = users_collection.find_one(
        {"_id": ObjectId(user["id"])},
        {"_id": 0, "password": 0, "picture": 0}
    )

    return schemas.ResponseModel(status="success", message="User successfully updated", data={"user": updated_user})

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(request: Request):
    user: dict = request.app.user
    users_collection: Collection = request.app.users_collection

    users_collection.delete_one({"_id": ObjectId(user["id"])})

    return None
