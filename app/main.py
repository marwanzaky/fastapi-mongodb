from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv

from app.routers.users import router as users_router
from app.routers.pages import router as pages_router

from pymongo import MongoClient
import os

load_dotenv('./.env')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(os.environ.get('MONGO_CLIENT_DB'), tls=True, tlsAllowInvalidCertificates=True)
    app.database = app.mongodb_client.app
    app.users_collection = app.database["users"]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(users_router)
app.include_router(pages_router)
